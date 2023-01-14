import csv
from datetime import datetime
import os
import re
import shutil
import subprocess
import threading
import time


def sudoCheck():
    if not "SUDO_IUD" in os.environ.keys():
        print("Access denied, Are you root?")
        exit()


def findNic():
    result = subprocess.run(["iw", "dev"], capture_output=True).stdout.decode()
    networkInterfaceControllers = wlan_code.findall(result)
    return networkInterfaceControllers


def setMonitorMode(controllerName):
    subprocess.run(["ip", "link", "set", wifiName, " down"])
    subprocess.run(["airmon-ng", "check", "kill"])
    subprocess.run(["iw", wifiName, "set", "monitor", "none"])
    subprocess.run(["ip", "link", "set", wifiName, "up"])


def setBandToMonitor(choice):
    if choice == "0":
        subprocess.Popen(["airodump-ng", " --band", "bg", "-w", "file", "--write-interval", "1",
                         "output-format", "csv", wifiName], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif choice == "T":
        subprocess.Popen(["airodump-ng", " --band", "bg", "-w", "file", "--write-interval", "1",
                         "output-format", "csv", wifiName], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def backupCsv():
    for fileName in os.listdir():
        if ".csv" in fileName:
            directory = os.getcwd()
            try:
                os.mkdir(directory + "/backup/")
            except:
                print("Backup Folder Exists")
                timestamp = datetime.now()
                shutil.move(fileName, directory + "/backup" + str(timestamp) + "-" + fileName)
                

def checkForEssid(essid, lst):
    checkStatus = True
    if len(lst) == 0:
        return checkStatus
    for item in lst:
        if essid in item["ESSID"]:
            checkStatus = False
    return checkStatus
