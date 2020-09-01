#!/bin/bash

if [[ $# > 0 ]]
then

	# Create temporary copy
	cp "$1" "$1.tmp"

	# Change line endings
	sed -i 's/\r//g' "$1.tmp"
	sed -i 's/\;$//g' "$1.tmp"

	# Remove first line
	sed -i '1,5d' "$1.tmp"



	# Import to sqlite
	cat <<EOF | sqlite3 "$1.db"
CREATE TABLE IF NOT EXISTS 'dump' (
StationMAC TEXT,
A1 TEXT,
A2 TEXT,
A3 TEXT,
A4 TEXT,
A5 TEXT,
A6 TEXT);
.mode csv
.separator ","
.import '$1.tmp' 'dump'
EOF


	# Remove copy
	rm -f "$1.tmp"
else
	# You need to specify the kismet.csv file
	echo "Argument is missing."
fi
