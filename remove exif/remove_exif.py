import os
from PIL import Image
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "images"))
files = os.listdir()

if len(files) == 0:
    print("No files found")
    exit()
    