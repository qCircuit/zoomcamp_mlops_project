import joblib
import mlflow
import numpy as np
import pandas as pd
import seaborn as sns
import time
import xgboost as xgb
from datetime import datetime
from prefect import flow, task
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

import utils

params = {
    "objective": "reg:squarederror",
    "eval_metric": "rmse",
    "max_depth": 7,
    "learning_rate": 0.1,
    "n_estimators": 300
}

@task(retries=3, retry_delay_seconds=2)
def get_data(file_path):
    st = time.time()
    data = pd.read_csv(file_path)
    data = data.loc[~data.Close.isna()].reset_index(drop=True)
    utils.logger.info(f"Data collected in {time.time()-st :.2f}s, its shape: {data.shape}" )

    return data

@task
def preprocess(data):
    st = time.time()
    utils.logger.info(f"Preprocessing started..." )
    # convert unix to datetime
    data["dt"] = data.Timestamp.apply(lambda x: datetime.fromtimestamp(x))

    # generate datetime features
    data["month"] = data.dt.apply(lambda v: v.month)
    data["day"] = data.dt.apply(lambda v: v.day)
    data["weekday"] = data.dt.apply(lambda v: v.weekday())
    data["hour"] = data.dt.apply(lambda v: v.hour)

    # drop non-significant columns
    data = data.drop(["Timestamp", "dt"], axis=1)

    # seet the target & split
    target = "Close"
    xtr, xts, ytr, yts = train_test_split(
        data.drop(target, axis=1),
        data[target],
        test_size=0.2,
        random_state=42
    )
    # save reference for grafana
    pd.concat([xts, yts], axis=1).to_parquet("data/reference.parquet", index=False)

    utils.logger.info(f"Data preprocessed in {time.time()-st :.2f}s" )
    utils.logger.info(f"Resulting shapes are {xtr.shape, xts.shape, ytr.shape, yts.shape}" )

    return xtr, xts, ytr, yts

@task(log_prints=True)
def fit_model(xtr, xts, ytr, yts):
    st = time.time()

    # init the pipeline
    pipeline = Pipeline([
        ("scaler", MinMaxScaler()), # normalization
        ("model", xgb.XGBRegressor(**params)) # fit
    ])

    # fit & predict
    pipeline.fit(xtr, ytr)
    ypr = pipeline.predict(xts)
    # check metrics
    metrics = {
        "mae": mean_absolute_error(yts, ypr),
        "mse": mean_squared_error(yts, ypr),
        "rmse": np.sqrt(mean_squared_error(yts, ypr))
    }

    file_path = "models/model.joblib"
    joblib.dump(pipeline, file_path)

    utils.logger.info(f"Model fitted in {time.time()-st :.2f}s" )
    utils.logger.info(f"...and saved as {file_path}" )
    utils.logger.info(f"Metrics are: {metrics}" )

    return pipeline, metrics

@task
def params_optim(xtr, xts, ytr, yts):
    st = time.time()

    # grid of parameters to optimize
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200, 300]
    }

    for i, params in enumerate(ParameterGrid(param_grid)):
        with mlflow.start_run():
            mlflow.set_tag("version", f"0.0.{i}")
            mlflow.log_params(params)

            # initialize and fit the model
            xgb_reg = xgb.XGBRegressor(objective='reg:squarederror', **params)
            xgb_reg.fit(xtr, ytr)
            ypr = xgb_reg.predict(xts)
            metrics = {
                "mae": mean_absolute_error(yts, ypr),
                "mse": mean_squared_error(yts, ypr),
                "rmse": np.sqrt(mean_squared_error(yts, ypr))
            }

            # logging metrics and models
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(xgb_reg, "model")
            joblib.dump(xgb_reg, "models/model.joblib")

    utils.logger.info(f"Params optimization completed in {time.time()-st :.2f}s" )

    return None

@flow
def train_sequence():
    data = get_data(file_path="data/bitcoin-historical-data.zip")
    data = preprocess(data)
    model, metrics = fit_model(data[0],data[1],data[2],data[3])

    return model, metrics
