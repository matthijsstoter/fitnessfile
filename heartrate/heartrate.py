from dataclasses import dataclass

import pandas as pd
import numpy as np

from .trimp import FactorBased, ZoneBased
from .timeinzones import TimeInZones

@dataclass
class HeartRate:

    _raw_data: pd.Series

    def __post_init__(self) -> None:
        self.data = self._raw_data.copy()

    def filter(self, hr_max: int) -> None:
        """Filter out heart rate values which are higher than the maximum heart rate"""
        self.data = self.data[self.data <= hr_max]

    def upsample(self) -> None:
        """Upsample the data in case there are missing values. I.e., when certain timestamps are missing"""
        actual_length = self.data.index.max() - self.data.index.min()  # The duration based on end time - start time
        index_length = len(self.data)  # Length of the index

        if actual_length != index_length:
            data = self.data.resample('1S').interpolate(method='time', limit_direction='both', axis=0).round()
            self.data = data
    
    @property
    def min(self) -> float:
        """Compute min heart rate"""
        return self.data.min()

    @property
    def max(self) -> float:
        """Compute max heart rate"""
        return self.data.max()
    
    @property
    def mean(self) -> float:
        """Compute mean heart rate"""
        return self.data.mean()
    
    @property
    def range(self) -> float:
        """Compute heart rate range"""
        return self.max - self.min
    
    @property
    def duration(self) -> float:
        """Compute duration"""
        return ((self.data.index.max() - self.data.index.min()).total_seconds() + 1) / 60
    
    def compute_delta_hr_ratio(self, hr_max: int, hr_rest: int) -> float:
        """Compute the delta heart rate ratio"""
        return (self.data.mean() - hr_rest) / (hr_max - hr_rest)
    
    def compute_factor_based_trimp(self, trimp: FactorBased, gender: str, hr_max: int, hr_min: int) -> float:
        """Compute any factor-based TRIMP score.
        Gender: Male / Female"""
        delta_hr_ratio = self.compute_delta_hr_ratio(hr_max, hr_min)
        factors = trimp.factors[gender]
        return self.duration * delta_hr_ratio * factors["A"] * np.exp(factors["B"] * delta_hr_ratio)

    def compute_zone_based_trimp(self, hr_max: int, trimp: ZoneBased) -> float:
        """Compute any zone-based TRIMP score"""
        time_in_zones = TimeInZones.compute(data=self.data, hr_max=hr_max, zones=trimp.zones)

        score: float = 0
        for idx, (_, time_in_zone) in enumerate(time_in_zones.items()):
            score += trimp.factors[idx] * time_in_zone
        
        return score
    
    def compute_percentage_heartrate_reserve(self, hr_max: int, hr_min: int) -> float:
        """Compute the percentage of Heart Rate Reserve"""
        return (self.mean - hr_min) / (hr_max - hr_min) * 100
    
    def compute_percentage_heartrate_max(self, hr_max: int) -> float:
        """Compute the  percentage of Heart rate max"""
        return self.mean / hr_max * 100
    
    def compute_heartrate_zones(self, hr_max: int, zones: list[float]) -> dict[str, float]:
        """Compute the time spent in heart rate zones"""
        return TimeInZones.compute(data=self.data, hr_max=hr_max, zones=zones)

    def compute_heartratereserve_zones(self, hr_max: int, hr_min: int, zones: list[float]) -> dict[str, float]:
        """Compute the time spent in heart rate zones"""
        zones = [zone * (hr_max - hr_min) + hr_min for zone in zones]
        return TimeInZones.compute(data=self.data, hr_max=hr_max, zones=zones)

