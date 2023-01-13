import os
from PIL import Image
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "images"))
files = os.listdir()

if len(files) == 0:
    print("No files found")
    exit()
    
for file in files:
    try:
        image = Image.open(file)
        imageData = list(image.getData())
        imageNoExif = Image.new(image.node, image.size)
        imageNoExif.putdata(imageData)
        imageNoExif.save(file)
    except IOError:
        print("unsurpoted file")