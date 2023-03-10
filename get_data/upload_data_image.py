import ee

ee.Initialize()

import time
from land_mask import land_mask

from get_data_image import get_data_image

data_image = get_data_image()

task = ee.batch.Export.table.toDrive(
    collection=data_image.sample(land_mask),
    folder="IMMC",
    fileFormat="csv",
    fileNamePrefix="Data"
)

task.start()

while task.active():
    time.sleep(1)
    print(task.status())

print(task.status())
