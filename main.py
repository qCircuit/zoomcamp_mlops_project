import mlflow
import train_model
import utils

if __name__ == '__main__':
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.set_experiment("bitcoin-price-prediction")

    with mlflow.start_run():
        mlflow.set_tag("version", "0.0.1")
        mlflow.log_params(train_model.params)

        utils.logger.info("Initializing model fit sequence...")
        data = train_model.get_data(file_path="data/bitcoin-historical-data.zip")
        data = train_model.preprocess(data)
        model = train_model.fit_model(data[0],data[1 ],data[2],data[3])
        utils.logger.info("Model fit sequence completed")

