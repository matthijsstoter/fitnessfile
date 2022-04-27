from abc import ABC


class FactorBased(ABC):
    name: str
    factors: dict[str, dict[str, float]]


class TRIMPBanister(FactorBased):
    name = "TRIMP Banister"
    factors = {"Male": {'A': 0.64, 'B': 1.92}, "Female": {'A': 0.86, 'B': 1.67}}


class TRIMPMorton(FactorBased):
    name = "TRIMP Morton"
    factors = {"Male": {'A': 2.718, 'B': 1.92}, "Female": {'A': 2.718, 'B': 1.67}}


class TRIMPStagno(FactorBased):
    name = "TRIMP Stango"
    factors = {"Male": {'A': 0.1225, 'B': 3.9434}, "Female": {'A': 0.1225, 'B': 3.9434}}


class ZoneBased(ABC):
    name: str
    zones: list[float]
    factors: list[float]


class TRIMPEdwards(ZoneBased):
    name = "TRIMP Edwards"
    zones = [0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
    factors = [1.0, 2.0, 3.0, 4.0, 5.0]


class TRIMPMod(ZoneBased):
    name = "TRIMP Edwards"
    zones = [0.65, 0.72, 0.79, 0.86, 0.93, 1.0]
    factors = [1.25, 1.71, 2.54, 3.61, 5.16]

