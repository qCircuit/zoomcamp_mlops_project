import unittest
from train_model_test import get_data, preprocess, train_sequence
import pandas as pd

# unit tests
class TestDataLoading(unittest.TestCase):

    def test_data_loading(self):
        data_path = "data/bitcoin-historical-data.zip"
        data = get_data(data_path)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn("Timestamp", data.columns)
        self.assertIn("Close", data.columns)

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "Timestamp": [1627618800, 1627618900, 1627619000],
            "Open": [10.0, 20.0, 30.0],
            "Close": [15.0, 25.0, 35.0]
        })

    def test_preprocess_shape(self):
        xtr, xts, ytr, yts = preprocess(self.data)
        self.assertEqual(xtr.shape[0] + xts.shape[0], self.data.shape[0])
        self.assertEqual(ytr.shape[0] + yts.shape[0], self.data.shape[0])
        self.assertEqual(ytr.shape[0], xtr.shape[0])
        self.assertEqual(yts.shape[0], xts.shape[0])

    def test_preprocess_datetime_features(self):
        xtr, xts, _, _ = preprocess(self.data)
        self.assertIn("month", xtr.columns)
        self.assertIn("day", xtr.columns)
        self.assertIn("weekday", xtr.columns)
        self.assertIn("hour", xtr.columns)

# integrity test
class TestTrainingSequence(unittest.TestCase):

    def test_training_sequence(self):
        model, metrics = train_sequence()
        self.assertIsNotNone(model)
        self.assertIsNotNone(metrics)
