
#### jammerDOSway
This tool can automatically drop devices connected to wifi networks around you from the wifi. All you have to do is meet the requirements, give permissions to the files and run it as root.
Have fun :>

###### REQUIREMENTS:
~python3

`sudo apt-get install python3`


~sqlite3 

`sudo apt-get install sqlite3`


~aircrack-ng

`sudo apt-get install aircrack-ng`


###### HaveToDo:

`chmod +x kismet2sqlite.sh`

`chmod +x kismet3sqlite.sh`


###### Run it:
Run the autodropper.py file as root with a few parameters. (You must be in the same path as this file!) 

parameters:

-t (targetname): Give the name of the wifi name you want to attack. (If you want to attack all WIFI devices around you do not use this parameter!)

-n (number of packages): Give the number of the DEAUTH packages will be send to the target(s).

`python3 autodropper.py -t <targetname> -n <number of packages you want>`
