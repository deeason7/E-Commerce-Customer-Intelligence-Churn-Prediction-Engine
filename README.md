# E-Commerce Customer Intelligence & Churn Prediction Engine

## Project Overview

This project transforms raw transactional data from a UK-based online retailer into a powerful **Customer Decision Intelligence Engine**. Moving beyond standard historical reporting, this analysis builds a comprehensive suite of tools to enable proactive, data-driven strategies.

The core of this project involves a deep dive into customer behavior to perform advanced segmentation, predict future customer value, identify churn risk, and uncover hidden product affinities. The final output is a set of actionable models and insights that can directly inform marketing, sales, and inventory management strategies to boost profitability and enhance customer retention.

---

## Business Questions Addressed

This project was designed to answer critical, high-level business questions:

1.  **Customer Value & Segmentation:** Who are our most valuable customers, and what are their distinct behavioral archetypes?
2.  **Churn Prediction:** Which of our high-value customers are at the greatest risk of leaving, and can we identify them proactively?
3.  **Product Affinity:** Which products are most frequently purchased together, and how can we leverage this to increase average order value?
4.  **Behavioral Drivers:** What are the key behaviors (e.g., purchase frequency, product variety) that are statistically linked to high long-term customer value?

---

## Tech Stack

* **Data Manipulation & Analysis:** `pandas`, `numpy`
* **Statistical Analysis:** `scipy`, `statsmodels`
* **Machine Learning:** `scikit-learn`
* **Market Basket Analysis:** `mlxtend`
* **Visualization:** `matplotlib`, `seaborn`, `squarify`

---

## Project Workflow & Methodology

The project follows a multi-phase, agile workflow, moving from foundational data engineering to advanced predictive modeling.

### 1: Data Engineering & Advanced Exploratory Data Analysis (EDA)

This phase focused on creating a pristine, analysis-ready dataset and uncovering foundational insights.

* **Robust Preprocessing:** Handled missing values, duplicates, and invalid entries. A key step was **outlier capping** using the IQR method to normalize distributions and reduce extreme skewness from over 300 down to ~1.1.
* **Advanced EDA Techniques:** Went beyond generic plots to uncover deep patterns:
    * **Pareto & Quadrant Analysis:** Confirmed that ~23% of products drive 80% of revenue and categorized the entire product catalog into strategic quadrants (Stars, Niche Winners, Volume Drivers, Underperformers).
    * **Time-Series Decomposition:** Quantitatively separated the monthly sales data into its **Trend, Seasonality, and Residual** components, revealing that the business's growth is primarily driven by seasonal spikes rather than a strong underlying trend.
    * **Customer Similarity Matrix (Computationally Intensive):** Built a **5857x5857** customer-to-customer correlation matrix based on purchasing habits. This computationally demanding step, involving millions of pairwise calculations, formed the basis for a prototype recommendation engine.

### 2: Region-Aware RFM Segmentation

To address the dataset's heavy geographical bias towards the UK, a sophisticated segmentation approach was implemented.

* **Region-Aware Scoring:** Customers were split into "UK" and "Rest of World" cohorts. RFM scores were calculated for each group *independently*, ensuring that international customers were scored fairly against their peers, not against the massive UK majority.
* **Actionable Segments:** Customers were categorized into 10 distinct segments, such as "Champions," "Loyal Customers," and "At-Risk," providing a clear framework for targeted marketing.

### 3: Hypothesis Testing

Used formal statistical tests to validate key business questions with rigor.

* **ANOVA Testing:** Moved beyond simple t-tests to use Analysis of Variance (ANOVA) to confirm that key metrics like **Average Purchase Value** and **Product Variety** were statistically different across the multiple customer segments.
* **Key Finding:** Confirmed that the primary drivers separating high-value from low-value customers are **Purchase Frequency** and **Product Variety**, not necessarily the amount they spend per transaction.

### 4: Predictive Churn Modeling

A complete, end-to-end machine learning pipeline was built to proactively identify customers at risk of churning.

* **Multi-Algorithm Benchmarking:** Trained and evaluated a suite of powerful classifiers (Logistic Regression, Random Forest, Gradient Boosting) using 5-fold cross-validation to select the best-performing algorithm.
* **Hyperparameter Tuning (Computationally Intensive):** Employed **GridSearchCV** to systematically search for the optimal parameters for the winning model (Gradient Boosting), ensuring maximum predictive performance.
* **Rigorous Evaluation:** The final, tuned model was evaluated on a held-out test set, achieving an exceptional **ROC AUC of 0.99+**. The evaluation included a detailed classification report, confusion matrix, ROC curve, and a feature importance analysis, which confirmed that **Recency** is the single most important predictor of churn.

### 5: Market Basket & Affinity Analysis

Uncovered hidden product relationships to power cross-selling strategies.

* **Apriori Algorithm:** Applied the Apriori algorithm to the transaction data to find frequent itemsets.
* **Association Rules:** Generated and filtered association rules to find product pairs with high **confidence** and **lift** (>56 for top pairs), resulting in a clean, actionable list of "if-then" recommendations (e.g., customers who buy "POPPY'S PLAYHOUSE LIVINGROOM" are extremely likely to buy the "KITCHEN").

---

[📊 Final Presentation](https://github.com/deeason7/E-Commerce-Customer-Intelligence-Churn-Prediction-Engine/tree/main/docs)

## How to Run This Project

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the notebooks:** Open the notebooks in the `notebooks/` directory and run the cells sequentially, starting with `Preprocessing.ipynb`.

---
