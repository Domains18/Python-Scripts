import socket
import ipaddress
import re

portRangePattern = re.compile(r"^\d{1,5}-\d{1,5}$")
portMin = 0
portMax = 65535

openPorts = []
while True:
    enteredIpAddr = input("Enter IP Address: ")
    try:
        objectIpAddr = ipaddress.ip_address(enteredIpAddr)
        print("Valid IP address")
        break
    except:
        print("Invalid IP address")
        
while True:
    print("Enter port range in the format of 'min-max'")
    portRange= input("Enter port range: ")
    if portRange == portRangePattern.search(portRange.replace(" ", "")):
        portMin = int(portRange.group().split("-")[0])
        portMax = int(portRange.group().split("-")[1])
        break
    
for port in range(portMin, portMax + 1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((enteredIpAddr, port))
        if result == 0:
            openPorts.append(port)
        sock.close()
    except:
        print(f"Port: {port} is closed")
        
for port in openPorts:
    print(f"Port: {port} is open")