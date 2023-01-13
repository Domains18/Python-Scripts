import nmap
import re

ipAddressPattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
portRangePattern = re.compile(r"^\d{1,5}-\d{1,5}$")
portMin = 0
portMax = 65535

openPorts = []
while  True:
    enteredIpAddr = input("Enter IP Address: ")
    if ipAddressPattern.match(enteredIpAddr):
        break
    
while True:
    print("Enter port range (ex: 1-1000): ")
    portRange = input("Enter port range: ")
    validPortRange = portRangePattern.search(portRange.replace(" ", ""))
    if validPortRange:
        portMin = int(validPortRange.group().split("-")[0])
        portMax = int(validPortRange.group().split("-")[1])
        break

nm = nmap.PortScanner()
for port in range(portMin, portMax + 1):
    try:
        result = nm.scan(enteredIpAddr, str(port))
        portStatus = (result["scan"][enteredIpAddr]["tcp"][port]["state"])
        print("Port: " + str(port) + " is " + portStatus)
    except:
        print(f"Port: {port} is closed")
        
