import pandas as pd


class TimeInZones:
    @staticmethod
    def create_zones(hr_max: int, zones: list[float], zone0: bool = False) -> list[float]:
        if zone0:
            zones.insert(0, 0)
        return [zone*hr_max for zone in zones]

    @staticmethod
    def name_zones(zones: list[float]) -> list[str]:
        offset = 1
        if 0 in zones:
            offset = 0
        return ["zone" + str(i+offset) for i, _ in enumerate(range(0, len(zones)-1))]
    
    @staticmethod
    def hr_in_range(data: pd.Series, lower_end: float, higher_end: float) -> pd.Series:
        """Assesses whether heart rates are within a certain range"""
        return (data >= lower_end) & (data < higher_end)  # Time zone
    
    @classmethod
    def create_hr_zone_dict(cls, hr_zones: list[float], hr_cols: list[str], data: pd.Series) -> dict[str, float]:
        hr: dict[str, float] = dict()
        for i in range(0, len(hr_zones)-1):
            hr[hr_cols[i]] = sum(cls.hr_in_range(data=data, lower_end=hr_zones[i], higher_end=hr_zones[i+1])) 
        return hr
    
    @classmethod
    def compute(cls, data: pd.Series, hr_max: int, zones: list[float]) -> dict[str, float]:
        hr_zones = cls.create_zones(hr_max=hr_max, zones=zones, zone0=False)
        hr_zone_names = cls.name_zones(hr_zones)
        time_in_zones = cls.create_hr_zone_dict(hr_zones=hr_zones, hr_cols=hr_zone_names, data=data)

        return time_in_zones
