import os
from PIL import Image

# replace with the actual path to the directory
path = "Pinterest"

min_height = 350
min_width = 350

# Remove images with the same name
# When downloading lots of images, any images with the same name will have a "(1)" appended to the name
# this removes the images with such numbers as they are percieved to be duplicates

for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        filepath = os.path.join(path, filename)

        # check if the file is a copy (if it contains "(1)", "(2)", or "(3)" after the name but before the period)
        if any(x in filename for x in ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"]):
            os.remove(filepath)
            print("Removed: " + filename)

# Remove images that are smaller than the minimum height and width

for file in os.listdir(path):
    if file.endswith(".jpg"):
        file_path = os.path.join(path, file)
        with Image.open(file_path) as img:
            width, height = img.size
            if (width < min_width or height < min_height):
                os.remove(file_path)
                print(f"{file} removed as it's smaller than 350x350.")

# Once Images that do not meet requirements or duplicates are removed,
# rename images to be numbered
i = 1
for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        os.rename(os.path.join(path, filename), os.path.join(path, f"{i:04d}.jpg"))
        i += 1

# Renamed images will be easier to keep track of during the manual filtering process
# You are now ready to start the manual filtering process