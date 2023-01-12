import subprocess
import winreg
import re
import codecs

print("Run With Administrator privileges")
print("To Whom Much is Given, Much Is Expected")

macToChangeTo = ["0A1122334455", "0E1122334455",
                 "021122334455", "061122334455"]
macAddresses = list()
macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")
transportName = re.compile("({.+})")
adapterIndex = re.compile("([0-9]+)")
getMacOutput = subprocess.run(
    "getmac", capture_output=True).stdout.decode().split("\n")
for macAdd in getMacOutput:
    macFind = macAddRegex.search(macAdd)
    transportFind = transportName.search(macAdd)
    if macFind == None or transportFind == None:
        continue
macAddresses.append((macFind.group(0), transportFind.group(0)))
print("Select MAc address to update")
for index, item in enumerate(macAddresses):
    print(f"{index} - Mac Address: {item[0]} - transport name: {item[1]}")

option = input(
    "Select The Menu item corresponding to the MAC that you want to change: ")

while True:
    print("Which MAC address do you want to use? This will change the Network Card's MAC address.")
    for index, item in enumerate(macToChangeTo):
        print(f"{index} - Mac Address: {item}")
    updateOption = input(
        "Select the Menu item Number corresponding to the MAC address the new MAC address that you want to use")
    if int(updateOption) >= 0 and int(updateOption) < len(macToChangeTo):
        print(f"Changing MAC address to : {macToChangeTo[int(updateOption)]}")
        break
    else:
        print("Invalid Option:")

controllerKeyPart = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    controllerKeyFolders = [("\\000" + str(item) if item <
                             10 else "\\00" + str(item)) for item in range(0, 21)]
    for keyFolder in controllerKeyFolders:
        try:
            with winreg.OpenKey(hkey, controllerKeyPart + keyFolder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                try:
                    count = 0
                    while True:
                        name, value, type = winreg.EnumValue(regkey, count)
                        count = count + 1
                        if name == "NetCfgInstanceId" and value == macAddresses[int(option)][1]:
                            newMacAddress = macToChangeTo[int(updateOption)]
                            winreg.SetValueEx(
                                regkey, "NetworkAddress", 0, winreg.REG_SZ, newMacAddress)
                            print("Succesfully matched Transport Number")
                            break
                except WindowsError:
                    pass
        except:
            pass

runDisableEnable = input(
    "Enable and Disable Your wireless interface? (y) for yes, ctrl +z to cancel")

if runDisableEnable.lower() == "y":
    runLastPart = True
else:
    runLastPart = False

while runLastPart:
    networkAdapters = subprocess.run(["wmic", "nic", "get", "name, index"], capture_output=True).stdout.decode(
        "utf-8", errors="ignore").split("\r\r\n")
    for adapter in networkAdapters:
        adapterIndexFind = adapterIndex.search(adapter.lstrip())
        if adapterIndexFind and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where",
                                     f"index={adapterIndexFind.group(0)}", "call", "disable"], capture_output=True)
            if (disable.returncode == 0):
                print(f"Disabled {adapter.lstrip()}")
                enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where",
                                        f"index={adapterIndexFind.group(0)}", "call", "disable"], capture_output=True)
                if (enable.returncode == 0):
                    print(f"Enabled{adapter.lstrip()}")
    getMacOutput = subprocess.run(
        "getmac", capture_output=True).stdout.decode()
    macAdd = "-".join([(macToChangeTo[int(updateOption)][i:i+2])
                      for i in range(0, len(macToChangeTo[int(updateOption)]), 2)])
    if macAdd in getMacOutput:
        print("Mac Address Success")
    break
