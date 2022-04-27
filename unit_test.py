import unittest
import os
import pathlib

import pandas as pd
from zmq import HEARTBEAT_IVL
from heartrate.heartrate import HeartRate

from trainingfile.trainingfile import TrainingFile
from trainingfile.readers import FitFileReader


FILE_DIR = pathlib.Path(os.getcwd()) / "data"
FILES = {f.split(".")[-1]: pathlib.Path(FILE_DIR / f) for f in os.listdir(FILE_DIR)}
FITFILE = FILES["fit"]


class TestTrainingFile(unittest.TestCase):

    def setUp(self):
        self.reader = FitFileReader(filepath=FITFILE)
        self.tr_file = TrainingFile(reader=self.reader)
    
    def test_data_is_dataframe(self):
        self.assertIsInstance(self.tr_file.data, pd.DataFrame)
    
    def test_training_type_is_string(self):
        self.assertIsInstance(self.tr_file.training_type, str)
    
    def test_duration_is_float(self):
        self.assertIsInstance(self.tr_file.duration, float)
    
    def test_hr_max_is_heartrate_instance(self):
        self.assertIsInstance(self.tr_file.heart_rate(), HeartRate)


class TestHeartRate(unittest.TestCase):
    def setUp(self):
        reader = FitFileReader(filepath=FITFILE)
        tr_file = TrainingFile(reader=reader)
        self.heartrate = HeartRate(tr_file.data["heart_rate"])
    
    def test_max_is_int(self):
        self.assertIsInstance(self.heartrate.max, int)
    
    def test_mean_is_pandas_series(self):
        self.assertIsInstance(self.heartrate.data, pd.Series)


if __name__ == "__main__":
    unittest.main()
    