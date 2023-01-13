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

