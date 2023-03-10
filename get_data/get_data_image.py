import ee
from process_image import process_image

def get_data_image() -> ee.Image:
    elevation = ee.Image("CGIAR/SRTM90_V4")
    slope = ee.Terrain.slope(elevation)
    aspect = ee.Terrain.aspect(elevation)
    land_cover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select("discrete_classification")
    
    daymet: ee.Image = ee.ImageCollection("NASA/ORNL/DAYMET_V4").filter(ee.Filter.date("2021-01-01T00:00:00", "2021-12-31T00:00:00"))
    
    sunlight = daymet.select("srad").reduce(ee.Reducer.mean())
    day_length = daymet.select("dayl").reduce(ee.Reducer.mean())

    rain = ee.Image("WORLDCLIM/V1/BIO").select("bio12")
    tree_cover = ee.ImageCollection("MODIS/006/MOD44B").limit(1, "system:time_start", False).first().select("Percent_Tree_Cover")

    return ee.Image.combine_([
        process_image(elevation, "elevation"),
        process_image(slope, "slope"),
        process_image(aspect, "aspect"),
        process_image(land_cover, "land_cover"),
        process_image(sunlight, "sunlight"),
        process_image(day_length, "day_length"),
        process_image(rain, "annual_precipitation"),
        process_image(tree_cover, "tree_cover")
    ])
