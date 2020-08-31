import subprocess
import os
import pandas as pd
import time
import signal

wifi_name = 'ceker'

def getInterfaceName():
    process_of_interface_output = subprocess.getoutput("iw dev | grep Interface")
    interface_name = process_of_interface_output.split("\n")[0]  # Searching for interface name
    interface_name = interface_name[11:]  # Getting the name only

    return interface_name

def changeMod(interface_name):
    os.system("airmon-ng start " + interface_name)

def isMonitor():
    process_of_type_output = subprocess.getoutput("iw dev | grep type")
    type_of_card = process_of_type_output.split("\n")[0]
    type_of_card = type_of_card[7:]
    print(type_of_card)
    if type_of_card == 'monitor':
        return True
    if type_of_card == 'managed':
        print("You may want change your type of network card manually.")
        return False

def scanNetwork(interface_name_monitor):
    print("Scanning...")
    command = ['airodump-ng','-w output_of_scan', interface_name_monitor]

    subprocess.run(command, timeout=3)
    print('ye')


interface_name = getInterfaceName()


changeMod(interface_name)

if isMonitor():
    print("The mode has changed to monitor instead of managed.")
    interface_name_monitor = interface_name

    scanNetwork(interface_name_monitor)
else:
    print("The mode has NOT changed to monitor instead of managed.\nYou may want change your type of network card manually.")

