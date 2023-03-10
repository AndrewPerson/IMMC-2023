import csv
from projects import projects
from data import Data

from itertools import count, takewhile


class frange:
    start: float
    stop: float
    step: float

    def __init__(self, start: float, stop: float, step: float):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return takewhile(lambda x: x < self.stop, count(self.start, self.step))

variables = {
    "solar_farm": {
        "solar_panel_efficiency": frange(0.15, 0.3, 0.01),
        "electricity_price": frange(20, 40, 1),
    },
    "farm": {
        "crop_yield": frange(0, 172.3 * 247.10538161, 1000),
        "crop_price": frange(4, 7, 0.5)
    },
    "agrivoltaic": {
        "solar_farm_percent": frange(0.5, 1, 0.05),
        "farm_percent": frange(0.5, 1, 0.05)
    }
}

data = Data.from_csv("./data.csv")

for project_name in projects:
    with open(f"{project_name}_sensitivity.csv", "w") as results_file:
        results_writer = csv.writer(results_file)

        project_variables = variables[project_name]
        project = projects[project_name]
        years = 100

        [var1name, var2name] = list(project_variables.keys())

        results_writer.writerow(["", *project_variables[var2name]])

        for var1 in project_variables[var1name]:
            setattr(project, var1name, var1)

            results = []

            for var2 in project_variables[var2name]:
                setattr(project, var2name, var2)

                results.append(sum(project.get_annual_profit(tile) * years - project.get_setup_cost(tile) - project.get_cleanup_cost(tile) for tile in data.tiles))

            results_writer.writerow([var1, *results])
