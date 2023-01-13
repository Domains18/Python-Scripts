import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

# def helper function


def createGoogleMapsUrl(gpsCoords):
    decDegLat = convertDecimalDegrees(float(gpsCoords["lat"][0])), float(
        gpsCoords["lat"][1]), float(gpsCoords["lat"][2]), gpsCoords(["latRef"])
    decDegLon = convertDecimalDegrees(float(gpsCoords["lon"][0])), float(
        gpsCoords["lon"][1]), float(gpsCoords["lon"][2]), gpsCoords(["lonRef"])
    return f"https://www.google.com/maps/place/{decDegLat},{decDegLon}"


def convertDecimalDegrees(degrees, minutes, seconds, direction):
    decimalDegrees = degrees + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimalDegrees *= -1
        return decimalDegrees


print("Starting...")
print("To Whom Much is Given, Much is Expected")

while True:
    outputChoice = input(
        "How do you want to receive the output:\n\n1 - File\n2 - Console\nEnter your choice: ")
    try:
        convVal = int(outputChoice)
        if convVal == 1:
            sys.stdout = open("exifData.txt", "w")
            break
        elif convVal == 2:
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid choice. Please try again.")

cwd = os.getcwd()
os.chdir(os.path.join(cwd, "images"))
files = os.listdir()

if len(files) == 0:
    print("No files found in images folder.")
    sys.exit()

for file in files:
    try:
        image = Image.open(file)
        print(f"Reading {file}...")
        gpsCoords = {}
        if image._getexif() == None:
            print("f{file} contains no exif data")
        else:
            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        print(f"{GPSTAGS.get(key)} - {val}")
                        if GPSTAGS.get(key) == "GPSLongitude":
                            gpsCoords["lon"] = val
                        elif GPSTAGS.get(key) == "GPSLatitude":
                            gpsCoords["lat"] = val
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gpsCoords["latRef"] = val
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gpsCoords["lonRef"] = val
                else:
                    print(f"{tag_name} - {value}")
            if gpsCoords:
                print(createGoogleMapsUrl(gpsCoords))
    except IOError:
        print("File Format not supported")

if outputChoice == "1":
    sys.stdout.close()
    os.chdir(cwd)
