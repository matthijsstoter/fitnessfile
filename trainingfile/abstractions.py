from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

import pandas as pd


class TrainingFileReader(ABC):
    """Abstract base class for all classes responsible for reading the training load file"""
    
    @abstractproperty
    def file_type(self) -> str:
        "Returns the filetype as a str"
    
    @abstractmethod
    def read_file(self) -> pd.DataFrame:
        """Reading the file containing the training load data into a Pandas DataFrame"""
    
    @abstractproperty
    def training_type(self) -> str:
        """Retrieving the training type"""
    
    @abstractproperty
    def start_time(self) -> datetime:
        "Retrieving the training start time"
    
    @abstractmethod
    def duration(self, raw_duration: float) -> float:
        "Computing the training duration"