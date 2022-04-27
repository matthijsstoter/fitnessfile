from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import pathlib

import pandas as pd

from .abstractions import TrainingFileReader
from heartrate.heartrate import HeartRate



@dataclass
class TrainingFile:
    reader: TrainingFileReader
    data: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.data: pd.DataFrame = self.reader.read_file()

    def __str__(self):
        return f"""This heart rate file describes a {self.training_type} training session, 
        which lasted for {self.duration} minutes and started at {self.start_time}."""
    
    @property
    def training_type(self) -> str:
        return self.reader.training_type

    @property
    def duration(self):
        raw_duration: float = self.data.index.max() - self.data.index.min()
        return self.reader.duration(raw_duration=raw_duration)

    @property
    def start_time(self) -> datetime:
        return self.reader.start_time
    
    def to_excel(self, filepath: pathlib.Path) -> None:
        self.data.to_excel(filepath)
    
    def heart_rate(self) -> Optional[HeartRate]:
        if "heart_rate" in self.data.columns:
            return HeartRate(self.data["heart_rate"].copy())
        else:
            return None
