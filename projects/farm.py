from project import Project
from data import DataTile


class Farm(Project):
    @classmethod
    def get_default(cls) -> "Project":
        return cls.get_corn()

    @classmethod
    def get_corn(cls) -> "Farm":
        # Seed cost from https://agecon.ca.uky.edu/grain-profitability-outlook-2022
        # Fertiliser cost calculated from https://agecon.ca.uky.edu/grain-profitability-outlook-2022
        # Extra costs from https://agecon.ca.uky.edu/grain-profitability-outlook-2022
        # Corn yield from https://www.dtnpf.com/agriculture/web/ag/crops/article/2022/11/16/acre-corn-cost-19-raise-2022-usda

        # Time for regeneration from https://www.openaccessgovernment.org/natural-regeneration/129359/
        # "species diversity takes 60 years"
        return cls(425021.26, 100 * 247.10538161, 100 * 0.9, 1543.25, 1000, 64.47, 273 * 247.10538161, 172.3 * 247.10538161, 6.60, 20, 2000, 60)
    
    @classmethod
    def get_soybean(cls) -> "Farm":
        return cls(0, 0, 0, 0, 0, 0, 0, 0, 0, 15.15)

    cost_to_setup: float # $/km^2
    seed_cost: float  # $/km^2
    water_for_crop: float  # ML/km^2
    water_cost: float  # $/ML
    fertiliser_for_crop: float  # kg/km^2
    fertiliser_cost: float  # $/kg
    extra_costs: float # $/km^2
    crop_yield: float  # bushels/km^2
    crop_price: float  # $/bushel
    trees_per_hectare: float # trees/ha
    tree_replant_cost: float # $/tree
    regeneration_time: float # years

    def __init__(self, cost_to_setup: float, seed_cost: float, water_for_crop: float, water_cost: float, fertiliser_for_crop: float, fertiliser_cost: float, extra_costs: float, crop_yield: float, crop_price: float, trees_per_hectare: float, tree_replant_cost: float, regeneration_time: float):
        self.cost_to_setup = cost_to_setup
        self.seed_cost = seed_cost
        self.water_for_crop = water_for_crop
        self.water_cost = water_cost
        self.fertiliser_for_crop = fertiliser_for_crop
        self.fertiliser_cost = fertiliser_cost
        self.extra_costs = extra_costs
        self.crop_yield = crop_yield
        self.crop_price = crop_price
        self.trees_per_hectare = trees_per_hectare
        self.tree_replant_cost = tree_replant_cost
        self.regeneration_time = regeneration_time

    def get_setup_cost(self, data_tile: DataTile) -> float:
        M2_PER_KM2 = 1000000
        km2_area = data_tile.area / M2_PER_KM2

        return self.cost_to_setup * km2_area

    def get_annual_profit(self, data_tile: DataTile) -> float:
        M2_PER_KM2 = 1000000 
        MM2_PER_M2 = 1000000
        ML_PER_MEGAL = 1000000000
        km2_area = data_tile.area / M2_PER_KM2

        crop_yield = self.crop_yield * km2_area
        rain = data_tile.annual_precipitation.value * data_tile.area * MM2_PER_M2 / ML_PER_MEGAL
        water = max(self.water_for_crop * km2_area - rain, 0)
        fertiliser = self.fertiliser_for_crop * km2_area

        return crop_yield * self.crop_price - self.seed_cost * km2_area - water * self.water_cost - fertiliser * self.fertiliser_cost - self.extra_costs * km2_area

    def get_cleanup_cost(self, data_tile: DataTile) -> float:
        M2_PER_HA = 10000
        trees = data_tile.area / M2_PER_HA * data_tile.tree_cover.value / 100 * self.trees_per_hectare

        return trees * self.tree_replant_cost + self.get_annual_profit(data_tile) * self.regeneration_time
