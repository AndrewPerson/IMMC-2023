from project import Project
from data import DataTile
from solar_farm import SolarFarm
from farm import Farm


class AgrivoltaicFarm(Project):
    @classmethod
    def get_default(cls) -> "Project":
        # Density appears appears for both appears to be the exact same as in a regular farm/solar farm.
        # TODO Find some more reliable statistics.

        return cls(SolarFarm.get_default(), .9, Farm.get_default(), 1)

    solar_farm_percent: float  # 0..1 for % of land covered by solar panels
    farm_percent: float  # 0..1 for % of land covered by farm

    solar_farm: SolarFarm
    farm: Farm

    def __init__(self, solar_farm: SolarFarm, solar_farm_percent: float, farm: Farm, farm_percent: float):
        self.solar_farm = solar_farm
        self.solar_farm_percent = solar_farm_percent
        self.farm = farm
        self.farm_percent = farm_percent

    def get_setup_cost(self, data_tile: DataTile) -> float:
        return self.solar_farm.get_setup_cost(data_tile) * self.solar_farm_percent + self.farm.get_setup_cost(data_tile) * self.farm_percent

    def get_annual_profit(self, data_tile: DataTile) -> float:
        return self.solar_farm.get_annual_profit(data_tile) * self.solar_farm_percent + self.farm.get_annual_profit(data_tile) * self.farm_percent

    def get_cleanup_cost(self, data_tile: DataTile) -> float:
        return self.solar_farm.get_cleanup_cost(data_tile) * self.solar_farm_percent + self.farm.get_cleanup_cost(data_tile) * self.farm_percent
