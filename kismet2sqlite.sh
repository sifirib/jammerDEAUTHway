#!/bin/bash
# This script converts *.kismet.csv files produced by airodump-ng into a sqlite database
# Usage: ./kismet2sqlite.sh myfile-01.kismet.csv
#
# Visit my website <hackherz.com> for more.
# © 2016 Daniel Stein <d.stein@hackherz.com>

if [[ $# > 0 ]]
then

	# Create temporary copy
	cp "$1" "$1.tmp"

	# Change line endings
	sed -i 's/\r//g' "$1.tmp"
	sed -i 's/\;$//g' "$1.tmp"

	# Remove first line
	sed -i 1d "$1.tmp"

	# Import to sqlite
	cat <<EOF | sqlite3 "$1.db"
CREATE TABLE IF NOT EXISTS 'dump' (
Network INTEGER PRIMARY KEY,
NetType TEXT,
ESSID TEXT,
BSSID TEXT,
Info TEXT,
Channel INTEGER,
Cloaked TEXT,
Encryption TEXT,
Decrypted TEXT,
MaxRate TEXT,
MaxSeenRate TEXT,
Beacon TEXT,
LLC TEXT,
Data TEXT,
Crypt TEXT,
Weak TEXT,
Total TEXT,
Carrier TEXT,
Encoding TEXT,
FirstTime TEXT,
LastTime TEXT,
BestQuality TEXT,
BestSignal TEXT,
BestNoise TEXT,
GPSMinLat TEXT,
GPSMinLon TEXT,
GPSMinAlt TEXT,
GPSMinSpd TEXT,
GPSMaxLat TEXT,
GPSMaxLon TEXT,
GPSMaxAlt TEXT,
GPSMaxSpd TEXT,
GPSBestLat TEXT,
GPSBestLon TEXT,
GPSBestAlt TEXT,
DataSize TEXT,
IPType TEXT,
IP TEXT);
.mode csv
.separator ";"
.import '$1.tmp' 'dump'
EOF


	# Remove copy
	rm -f "$1.tmp"
else
	# You need to specify the kismet.csv file
	echo "Argument is missing."
fi
