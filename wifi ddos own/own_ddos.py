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
                shutil.move(fileName, directory + "/backup" +
                            str(timestamp) + "-" + fileName)


def checkForEssid(essid, lst):
    checkStatus = True
    if len(lst) == 0:
        return checkStatus
    for item in lst:
        if essid in item["ESSID"]:
            checkStatus = False
    return checkStatus


def wifiNetworkMenu():
    activeWirelessNetworks = []
    try:
        while True:
            subprocess.call("clear", shell=True)
            for fileName in os.listdir():
                fieldNames = ["BSSID", "First time seen", "Last time seen",
                              "channel", "Speed", "Privacy", "Cipher",]
                if ".csv" in fileName:
                    with open(fileName, "r") as file:
                        reader = csv.DictReader(file, fieldnames=fieldNames)
                        for row in reader:
                            if row["BSSID"] != "BSSID":
                                if checkForEssid(row["BSSID"], activeWirelessNetworks):
                                    activeWirelessNetworks.append(row)
            print("Scanning for wireless networks...")
            for index, network in enumerate(activeWirelessNetworks):
                print(f"{index + 1} - {network['BSSID']}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Ready To Make Choice")
    
    while True:
        try:
            choice = int(input("Enter the number of the network you want to attack: "))
            if choice > 0 and choice <= len(activeWirelessNetworks):
                return activeWirelessNetworks[choice - 1]
        except:
            print("Invalid Choice")
            
def setIntoManagedMode(wifiName):
    subprocess.run(["airmon-ng", "stop", wifiName])
    subprocess.run(["ip", "link", "set", wifiName, "down"])
    #moniter mode
    subprocess.run(["iwconfig", wifiName, "mode", "managed"])
    subprocess.run(["ip", "link", "set", wifiName, "up"])
    subprocess.run(["service", "network-manager", "restart"])
    