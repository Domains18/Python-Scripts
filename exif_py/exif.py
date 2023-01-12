import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

# def helper function
def createGoogleMapsUrl(gpsCoords):
    decDegLon = convertDecimalDegrees(float(gpsCoords["lat"][0])), float(gpsCoords["lat"][1]), float(gpsCoords["lat"][2]), gpsCoords(["latRef"])
    decDegLon = convertDecimalDegrees(float(gpsCoords["lon"][0])), float(gpsCoords["lon"][1]), float(gpsCoords["lon"][2]), gpsCoords(["lonRef"])