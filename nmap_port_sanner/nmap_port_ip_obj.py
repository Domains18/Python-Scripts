import nmap
import ipaddress
import re

portRangePattern = re.compile(r"^\d{1,5}-\d{1,5}$")
portMin = 0
portMax = 65535

while True:
    enteredIpAddr = input("Enter IP Address: ")
    try:
        ipAddrObject = ipaddress.ip_address(enteredIpAddr)
        print("You entered a valid IP address")
        break
    except:
        print("Invalid IP address")

while True:
    print("Enter port range in the format of 'min-max'")
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
        
# Output:
