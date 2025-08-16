# app/data_loader.py
import pandas as pd
import joblib
import logging
import os

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    """
    Loads all necessary CSV files into pandas DataFrames.
    Returns a dictionary of DataFrames
    """
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    master_file_path = os.path.join(PROJECT_ROOT, "data", "processed", "master_data.csv")

    print("Looking for:", master_file_path)  # debug
    if not os.path.exists(master_file_path):
        raise FileNotFoundError(f"File not found at {master_file_path}")

    data_files = {
        'master': master_file_path,
        'churn': 'data/churn_predictions.csv',
        'rules': 'data/association_rules.csv'
    }
    dataframes = {}

    for name, path in data_files.items():
        try:
            df = pd.read_csv(path)
            if 'InvoiceDate' in df.columns:
                df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

            dataframes[name] = df
            logging.info(f"Successfully loaded {path}")

        except FileNotFoundError:
            logging.error(f"Error: The file at {path} was not found.")

            # Create an empty DataFrame
            dataframes[name] = pd.DataFrame()

    # Load the trained model
    try:
        model = joblib.load('churn_model.pkl')
        dataframes['churn_model'] = model
        logging.info("Successfully loaded churn_model.pkl")
    except FileNotFoundError:
        logging.error("Error: churn_model.pkl was not found.")
        dataframes['churn_model'] = None

    return dataframes