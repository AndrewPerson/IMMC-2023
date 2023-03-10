from project import Project
from data import DataTile
import math

class SolarFarm(Project):
    @classmethod
    def get_default(cls) -> "Project":
        #Cost of installation from https://www.angi.com/articles/cost-solar-farm.htm
        #Also from https://arena.gov.au/renewable-energy/large-scale-solar/

        # Solar panel density from https://ieeexplore.ieee.org/document/9676427
        # Although ground coverage ratios vary from site to site, depending on terrain and other factors, they typically range from 0.40 to 0.50 for fixed-tilt plants versus 0.25–0.40 for tracking plants 

        #Solar panel efficiency from https://solarcalculator.com.au/solar-panel-efficiency/
        #Assume to be 20% for now

        #Costs for electricity from https://www.eia.gov/todayinenergy/detail.php?id=46396

        #Maintenance costs from https://www.scottmadden.com/insight/solar-photovoltaic-plant-operating-and-maintenance-costs/

        #Also check ballpark figures from https://www.skystreamenergy.com/how-many-acres-are-needed-for-a-1-mw-solar-farm/

        # Trees per hectare from TODO
        # Tree replanting cost from TODO

        # Time for regeneration from https://www.openaccessgovernment.org/natural-regeneration/129359/
        # "species diversity takes 60 years"

        return cls(1.3, 0.45, 0.2, 30, 52/8766*1000, 20, 2000, 60)

    installation_cost_per_w: float # $/W
    solar_panel_density: float # 0..1 for % land covered
    solar_panel_efficiency: float # 0..1 for % of sunlight converted to electricity
    electricity_price: float # $/MWh
    maintenance_per_mw: float # $/MWh
    trees_per_hectare: float # trees/ha
    tree_replant_cost: float # $/tree
    regeneration_time: float # years

    def __init__(self, installation_cost_per_w: float, solar_panel_density: float, solar_panel_efficiency: float, electricity_price: float, maintenance_per_mw: float, trees_per_hectare: float, tree_replant_cost: float, regeneration_time: float):
        self.installation_cost_per_w = installation_cost_per_w
        self.solar_panel_density = solar_panel_density
        self.solar_panel_efficiency = solar_panel_efficiency
        self.electricity_price = electricity_price
        self.maintenance_per_mw = maintenance_per_mw
        self.trees_per_hectare = trees_per_hectare
        self.tree_replant_cost = tree_replant_cost
        self.regeneration_time = regeneration_time

    def get_setup_cost(self, data_tile: DataTile) -> float:
        watts = data_tile.sunlight.value * data_tile.area * self.solar_panel_density * self.solar_panel_efficiency

        return watts * self.installation_cost_per_w

    def get_annual_profit(self, data_tile: DataTile) -> float:
        angle_to_sun = abs(data_tile.slope.value * math.sin(math.radians(data_tile.aspect.value)))
        time_in_sun = 24 * (180 - angle_to_sun) / 360

        HOURS_PER_YEAR = time_in_sun * 365.25
        WATTS_PER_MW = 1000000

        mega_watt_hours_per_year = data_tile.sunlight.value * data_tile.area * self.solar_panel_density * self.solar_panel_efficiency * HOURS_PER_YEAR / WATTS_PER_MW

        maintenance = mega_watt_hours_per_year * self.maintenance_per_mw

        income = mega_watt_hours_per_year * self.electricity_price

        return income - maintenance

    #TODO Take into account taking down the solar array
    def get_cleanup_cost(self, data_tile: DataTile) -> float:
        M2_PER_HA = 10000
        trees = data_tile.area / M2_PER_HA * data_tile.tree_cover.value / 100 * self.trees_per_hectare

        return trees * self.tree_replant_cost + self.get_annual_profit(data_tile) * self.regeneration_time
