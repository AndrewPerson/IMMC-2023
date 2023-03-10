from project import Project
from solar_farm import SolarFarm
from farm import Farm
from agrivoltaic import AgrivoltaicFarm


projects: dict[str, Project] = {
    "solar_farm": SolarFarm.get_default(),
    "farm": Farm.get_default(),
    "agrivoltaic": AgrivoltaicFarm.get_default()
}
