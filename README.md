
#### jammerDOSway
This tool can automatically drop devices connected to wifi networks around you from the wifi. All you have to do is meet the requirements, give permissions to the files and run it as root.
Have fun :>

### Important Note: 
It is illegal to monitor and / or record interpersonal communication without providing the necessary procedures, and committing this act constitutes a crime.

The users are deemed to have accepted the legal liabilities, material, moral and any possible damages that may arise from the legal and illegal use of this tool, and the developers cannot be held responsible in any way.

Any damages and liabilities arising from the use of this code belong to the users.

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


###### RUN IT:
Run the autodropper.py file as root with a few parameters. (You must be in the same path as this file!) 

parameters:

-t (targetname): Give the name of the wifi name you want to attack. (If you want to attack all WIFI devices around you do not use this parameter!)

-n (number of packages): Give the number of the DEAUTH packages will be send to the target(s).

`python3 autodropper.py -t <target name> -n <number of the packages>`
