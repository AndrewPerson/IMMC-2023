import csv


class DataTileLayer:
    # area: m^2
    def __init__(self, value: float, area: float, lat: float, lon: float):
        self.value = value
        self.area = area
        self.lat = lat
        self.lon = lon


class DataTile:
    # area: m^2
    def __init__(self, area: float, annual_precipitation: DataTileLayer, aspect: DataTileLayer, day_length: DataTileLayer, elevation: DataTileLayer, land_cover: DataTileLayer, slope: DataTileLayer, sunlight: DataTileLayer, tree_cover: DataTileLayer):
        self.area = area

        self.annual_precipitation = annual_precipitation
        self.aspect = aspect
        self.day_length = day_length
        self.elevation = elevation
        self.land_cover = land_cover
        self.slope = slope
        self.sunlight = sunlight
        self.tree_cover = tree_cover


class Data:
    def __init__(self, tiles: list[DataTile]):
        self.tiles = tiles

    @classmethod
    def from_csv(cls, path: str):
        with open(path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            next(csv_reader)

            data: dict[str, list[DataTileLayer]] = {
                "annual_precipitation": [],
                "aspect": [],
                "day_length": [],
                "elevation": [],
                "land_cover": [],
                "slope": [],
                "sunlight": [],
                "tree_cover": []
            }

            for row in csv_reader:
                row_index = 1
                for key in data:
                    data[key].append(DataTileLayer(
                        float(row[row_index]), float(row[row_index + 1]), float(
                            row[row_index + 2]), float(row[row_index + 3])
                    ))

                    row_index += 4

            tiles = []
            for layers in zip(*data.values()):
                area = min([layer.area for layer in layers])

                tiles.append(DataTile(area, *layers))

            return cls(tiles)
