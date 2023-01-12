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
