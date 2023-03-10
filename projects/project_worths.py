from project import Project
from projects import projects
from data import Data
import csv

data = Data.from_csv("./data.csv")

years = int(input("Number of years: "))

def get_total_worth_for_tiles(project: Project, years: int, data: Data):
    #return [project.get_annual_profit(tile) * years for tile in data.tiles]
    return [project.get_annual_profit(tile) * years - project.get_setup_cost(tile) - project.get_cleanup_cost(tile) for tile in data.tiles]

for project_name in projects:
    with open(f"{project_name}_results.csv", "w") as results_file:
        results_writer = csv.writer(results_file)

        results_writer.writerow(["Tile Index", "Setup Cost", *[f"Year {year + 1}" for year in range(years)], "Cleanup Cost"])

        project = projects[project_name]
        
        for i in range(len(data.tiles)):
            tile = data.tiles[i]

            results_writer.writerow([i, project.get_setup_cost(tile), *[project.get_annual_profit(tile) * (year + 1) for year in range(years)], project.get_cleanup_cost(tile)])
