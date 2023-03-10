from abc import ABC, abstractmethod
from data import DataTile

class Project(ABC):
    @classmethod
    @abstractmethod
    def get_default(cls) -> "Project":
        pass

    @abstractmethod
    def get_setup_cost(self, data_tile: DataTile) -> float:
        pass

    @abstractmethod
    def get_annual_profit(self, data_tile: DataTile) -> float:
        pass

    @abstractmethod
    def get_cleanup_cost(self, data_tile: DataTile) -> float:
        pass