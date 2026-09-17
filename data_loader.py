import pandas as pd


def load_sales_data(file_path):
    df = pd.read_csv(file_path)
    return df