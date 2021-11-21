# TO CREATE train.txt and test.txt for training datasets with YOLO

import glob
import os

directory_path = r"C:\Users\Nico\darknet\build\darknet\x64\data\obj"

with open("output.txt", "w") as f:

    files = glob.glob(directory_path + "/**/*.jpg", recursive=True)

    for file in files:

        f.write(str(file + "\n"))

    #
    #     filename = os.path.split(file)[-1]
    #
    #     yolo_path = os.path.join("data/obj/" + filename)
    #
    #     f.write(str(yolo_path + "\n"))
