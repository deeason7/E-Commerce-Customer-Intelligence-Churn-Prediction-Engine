# app/routes.py
from flask import Blueprint, render_template
from . import DATA
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import logging
from flask import request

main_bp = Blueprint('main', __name__)


# Home Page Route
@main_bp.route('/')
def index():
    master_df = DATA['master']
    kpis = {
        'total_revenue': master_df['TotalPrice'].sum() if not master_df.empty else 0,
        'unique_customers': master_df['Customer ID'].nunique() if not master_df.empty else 0,
        'total_transactions': master_df['Invoice'].nunique() if not master_df.empty else 0,
    }

    sales_chart_html = "<div>Monthly sales data not available.</div>"
    if not master_df.empty:
        monthly_sales = master_df.set_index('InvoiceDate').resample('M')['TotalPrice'].sum().reset_index()
        fig_sales = px.line(monthly_sales, x='InvoiceDate', y='TotalPrice', title="Monthly Sales Trend",
                            labels={'InvoiceDate': 'Month', 'TotalPrice': 'Total Revenue'})
        sales_chart_html = fig_sales.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('index.html', kpis=kpis, sales_chart=sales_chart_html)


# Churn Analysis Page Route
@main_bp.route('/churn')
def churn_analysis():
    churn_df = DATA['churn'].copy()
    master_df = DATA['master']
    churn_model = DATA['churn_model']

    treemap_html = "<div>Customer segment data not available.</div>"
    if not churn_df.empty and not master_df.empty:
        # RFM Segmentation Logic
        churn_df['R_Score'] = pd.qcut(churn_df['Recency'], 5, labels=[5, 4, 3, 2, 1])
        churn_df['F_Score'] = pd.qcut(churn_df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

        segment_map = {
            r'[1-2][1-2]': 'Hibernating', r'[1-2][3-4]': 'At-Risk', r'[1-2]5': 'Cannot Lose Them',
            r'3[1-2]': 'About to Sleep', r'33': 'Need Attention', r'[3-4][4-5]': 'Loyal Customers',
            r'41': 'Promising', r'51': 'New Customers', r'[4-5][2-3]': 'Potential Loyalists',
            r'5[4-5]': 'Champions'
        }
        churn_df['Segment'] = churn_df['R_Score'].astype(str) + churn_df['F_Score'].astype(str)
        churn_df['Segment'] = churn_df['Segment'].replace(segment_map, regex=True)

        # Calculate Revenue per Segment
        # First, get total revenue per customer from the master data
        customer_revenue = master_df.groupby('Customer ID')['TotalPrice'].sum().reset_index()

        # Merge revenue data into the churn dataframe
        churn_df_with_revenue = pd.merge(churn_df, customer_revenue, on='Customer ID', how='left')

        # Aggregate by segment to get count and total revenue
        segment_data = churn_df_with_revenue.groupby('Segment').agg(
            Count=('Customer ID', 'nunique'),
            TotalRevenue=('TotalPrice', 'sum')
        ).reset_index()

        # ENHANCED Treemap
        fig_treemap = px.treemap(
            segment_data,
            path=['Segment'],
            values='Count',
            color='TotalRevenue',  
            hover_data={'TotalRevenue': ':.2f'},  
            color_continuous_scale='RdYlGn',  
            title='Customer Segments by Count and Total Revenue'
        )

        fig_treemap.update_traces(
            textinfo="label+value+percent root",
            hovertemplate='<b>%{label}</b><br>Customer Count: %{value}<br>Total Revenue: %{customdata[0]:$,.2f}<extra></extra>'
        )
        treemap_html = fig_treemap.to_html(full_html=False, include_plotlyjs='cdn')

    # Feature Importance Chart
    feature_importance_html = "<div>Churn model not loaded.</div>"
    if churn_model:
        feature_names = ['Recency', 'Frequency', 'Monetary']
        importances = churn_model[-1].feature_importances_
        feature_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values(by='importance',
                                                                                                     ascending=False)
        fig_importance = px.bar(feature_df, x='feature', y='importance', title='Key Drivers of Customer Churn',
                                labels={'feature': 'Factor', 'importance': 'Importance Score'})
        feature_importance_html = fig_importance.to_html(full_html=False, include_plotlyjs='cdn')

    churn_table_html = churn_df.to_html(classes='table table-sm table-hover', index=False, table_id='churnTable')

    return render_template('churn.html', treemap=treemap_html, feature_importance_chart=feature_importance_html,
                           churn_table=churn_table_html)


# Affinity Analysis Page Route
@main_bp.route('/affinity', methods=['GET'])
def affinity_analysis():
    rules_df = DATA['rules']

    # Get a unique, sorted list of all products that are antecedents
    product_list = sorted(rules_df['antecedents'].unique())

    # Get the product selected by the user from the dropdown
    selected_product = request.args.get('product', None)

    recommendations = []
    bar_chart_html = None 

    if selected_product:
        # Filter the rules to find recommendations for the selected product
        recommendations_df = rules_df[rules_df['antecedents'] == selected_product].sort_values(by='lift',
                                                                                               ascending=False)

        # Create the recommendation bar chart
        if not recommendations_df.empty:
            # Top 5 for the chart
            top_5_for_chart = recommendations_df.head(5).sort_values(by='lift', ascending=True)
            fig_bar = px.bar(
                top_5_for_chart,
                x='lift',
                y='consequents',
                orientation='h',
                title=f'Top 5 Recommendations for "{selected_product}"',
                labels={'consequents': 'Recommended Product', 'lift': 'Strength of Association (Lift)'}
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})  # Ensure highest lift is on top
            bar_chart_html = fig_bar.to_html(full_html=False, include_plotlyjs='cdn')

        # Convert the filtered dataframe into a list of dictionaries for the cards
        for _, row in recommendations_df.iterrows():
            recommendations.append({
                'item': row['consequents'],
                'lift': round(row['lift'], 2),
                'confidence': f"{round(row['confidence'] * 100, 1)}%"
            })

    return render_template('affinity.html',
                           product_list=product_list,
                           selected_product=selected_product,
                           recommendations=recommendations,
                           bar_chart=bar_chart_html)