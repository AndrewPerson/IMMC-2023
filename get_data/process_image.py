import ee

def process_image(image: ee.Image, name: str):
    return ee.Image.combine_([
        image.rename(name),
        image.pixelArea().rename(f"{name}_area"),
        image.pixelLonLat().rename([
            f"{name}_lon",
            f"{name}_lat"
        ])
    ])