#!/usr/bin/env bash
#Run this script as root.

APT_GET=$(which apt-get)
APT=$(which apt)
YUM=$(which yum)
DNF=$(which dnf) 
PKG=$(which pkg)
MAKE=$(which make)

if [[ ! -z $YUM ]]; then
  yum check-update
  yum install python3 sqlite3 net-tools aircrack-ng sqlite3 gnome-terminal
  exit 1;
elif [[ ! -z $APT_GET ]]; then
  apt-get update
  apt-get install python3 sqlite3 net-tools aircrack-ng sqlite3 gnome-terminal
  exit 1;
elif [[ ! -z $APT ]]; then
  apt update
  apt install python3 sqlite3 net-tools aircrack-ng sqlite3 gnome-terminal
  exit 1;
elif [[ ! -z $DNF ]]; then
  dnf check-update
  dnf install python3 sqlite3 net-tools aircrack-ng sqlite3 gnome-terminal
  exit 1;
elif [[ ! -z $PKG ]]; then
  pkg update
  pkg install python3 sqlite3 net-tools aircrack-ng sqlite3 gnome-terminal
  exit 1;
else
  echo "Cannot install packages! Try install them manually."
  exit 1;
fi

