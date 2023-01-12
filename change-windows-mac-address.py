import subprocess
import winreg
import re
import codecs

print("Run With Administrator privileges")
print("To Whom Much is Given, Much Is Expected")

macToChangeTo = ["0A1122334455", "0E1122334455", "021122334455", "061122334455"]
macAddresses = list()
macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")
transportName = re.compile("({.+})")
adapterIndex = re.compile("([0-9]+)")
getMacOutput = subprocess.run("getmac", capture_output=True).stdout.decode().split("\n")
for macAdd in getMacOutput:
    macFind = macAddRegex.search(macAdd)
    transportFind = transportName.search(macAdd)
    if macFind == None or transportFind == None:
        continue
macAddresses.append((macFind.group(0), transportFind.group(0)))
print("Select MAc address to update")
for index, item in enumerate(macAddresses):
    print(f"{index} - Mac Address: {item[0]} - transport name: {item[1]}")
    
option = input("Select The Menu item corresponding to the MAC that you want to change: ")

while True:
    print("Which MAC address do you want to use? This will change the Network Card's MAC address.")
    for index, item in enumerate(macToChangeTo):
        print(f"{index} - Mac Address: {item}")
    updateOption = input("Select the Menu item Number corresponding to the MAC address the new MAC address that you want to use")
    if int(updateOption) >= 0 and int(updateOption) < len(macToChangeTo):
        print(f"Changing MAC address to : {macToChangeTo[int(updateOption)]}")
        break
    else:
        print("Invalid Option:")
        