
#### jammerDOSway
This tool can automatically drop devices connected to all wifi networks around you from the wifi. All you have to do is meet the requirements, give permissions to the files and run it as root.
Have fun :>

## Features:

+You can change your MAC address by giving an address you want.

+You can change quality of the attack by giving number between 1 and 20.

+You can attack only a specific target by giving name of the WIFI correctly.

+You can determine how many packages will be sent to the target(s).


### Important Note: 
It is illegal to monitor and / or record interpersonal communication without providing the necessary procedures, and committing this act constitutes a crime.

The users are deemed to have accepted the legal liabilities, material, moral and any possible damages that may arise from the legal and illegal use of this tool, and the developers cannot be held responsible in any way.

Any damages and liabilities arising from the use of this code belong to the users.
### HaveToDo: 

Make bash scripts executable. Run following command as root.

`chmod +x install.sh kismet2sqlite.sh kismet3sqlite.sh`

### REQUIREMENTS:

#### You can install all of required packages automatically by running install.sh as root:

`bash install.sh`

#### Or install them manually:

`sudo apt-get install python3 sqlite3 aircrack-ng net-tools gnome-terminal`


## Run it / Usage :
Run the autodropper.py file as root with a few parameters. (You must be in the same path as this file!) 

`python3 autodropper.py -t <target name> -n <number of the packages> -m <mac address you want to change with> -q <quality value>`

`python3 autodropper.py -t office -n 1200 -m aa:bb:cc:dd:ee:ff -q 8`


##### parameters:

-t or --target : Give the name of the wifi name you want to attack. (If you want to attack all WIFI devices around you do not use this parameter!)

-n or --number : Give the number of the DEAUTH packages will be send to the target(s).

-m or --mac : Temporary new MAC address you want to change with.

-q or --quality : Enter a number between 1 and 20. The higher the number, the higher the quality of the attack as well as the time taken!(default=1)


