import os
import csv 
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

def createGooglrMapUrl(gpsCoordinates):
    decDegLat = convertToDecDeg(float(gpsCoordinates["lat"][0]), float(gpsCoordinates["lat"][1]), float(gpsCoordinates["lat"][2]), gpsCoordinates["latRef"])
    decDegLon = convertToDecDeg(float(gpsCoordinates["lon"][0]), float(gpsCoordinates["lon"][1]), float(gpsCoordinates["lon"][2]), gpsCoordinates["lonRef"])
    return f"https://www.google.com/maps/place/{decDegLat},{decDegLon}"

def convertToDecDeg(deg, min, sec, ref):
    decDeg = deg + (min / 60) + (sec / 3600)
    if ref in ["S", "W"]:
        decDeg *= -1
    return decDeg

cwd = os.getcwd()
os.chdir(os.path.join(cwd, "images"))
files = os.listdir()

if len(files) == 0:
    print("No images found in images folder")
    exit()
    
with open("exif.csv", "w", newline="") as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(["File Name", "Date Taken", "Latitude", "Longitude", "Google Maps URL"])
    for file in files:
        try:
            image = Image.open(file)
            exifData = image._getexif()
            gpsData = {}
            for tagId, value in exifData.items():
                tag = TAGS.get(tagId, tagId)
                if tag == "GPSInfo":
                    for t in value:
                        subTag = GPSTAGS.get(t, t)
                        gpsData[subTag] = value[t]
            csvWriter.writerow([file, exifData[36867], gpsData["GPSLatitude"], gpsData["GPSLongitude"], createGooglrMapUrl(gpsData)])
        except:
            print(f"Error reading exif data from {file}")
            
os.chdir(cwd)