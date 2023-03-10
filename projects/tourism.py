from project import Project
from data import DataTile


#TODO: Implement this class
class Tourism(Project):
    @classmethod
    def get_default(cls) -> "Project":
        return cls()
    
    def __init__(self):
        raise NotImplementedError()

    def get_setup_cost(self, data_tile: DataTile) -> float:
        return super().get_setup_cost(data_tile)
    
    def get_annual_profit(self, data_tile: DataTile) -> float:
        return super().get_annual_profit(data_tile)
    
    def get_cleanup_cost(self, data_tile: DataTile) -> float:
        return super().get_cleanup_cost(data_tile)
