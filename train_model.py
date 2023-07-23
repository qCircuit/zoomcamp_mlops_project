import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler

import logging

def setup_logger(log_file):
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    return logger

logger = setup_logger("logs.log")

def get_data(file_path):
    data = pd.read_csv(file_path)
    data = data.loc[~data.Close.isna()].reset_index(drop=True)
    logger.info(data.shape)
    
    return df

data = get_data(file_path="data/bitcoin-historical-data.zip")