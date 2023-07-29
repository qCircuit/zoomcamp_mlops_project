import mlflow
import train_model
import utils

import unittest
import unit_tests

'''
1: "parameters optimization",
2: "final model training"
3: "unit tests"
'''
MODE = 3

if __name__ == '__main__':
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.set_experiment("bitcoin-price-prediction")

    if MODE == 1:
        utils.logger.info("Initializing parameter optimization sequence...")
        data = train_model.get_data(file_path="data/bitcoin-historical-data.zip")
        data = train_model.preprocess(data)
        train_model.params_optim(data[0],data[1],data[2],data[3])
        utils.logger.info("Parameters optimization sequence completed")

    elif MODE == 2:
        with mlflow.start_run():
            mlflow.set_tag("version", "0.1.0")
            mlflow.log_params(train_model.params)
            utils.logger.info("Initializing model fit sequence...")
            model, metrics = train_model.train_sequence()
            utils.logger.info("Model fit sequence completed")

    elif MODE == 3:
        suite = unittest.TestLoader().loadTestsFromModule(unit_tests)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
