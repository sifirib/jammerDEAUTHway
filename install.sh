#!/bin/bash
#Run this script as root.

APT_GET=$(which apt-get)
APT=$(which apt)
YUM=$(which yum)
DNF=$(which dnf) 
PKG=$(which pkg)
MAKE=$(which make)
PACMAN=$(which pacman)

if [[ ! -z $YUM ]]; then
  yum check-update
  yum install - < requirements.txt
  exit 1;
elif [[ ! -z $APT_GET ]]; then
  apt-get update
  apt-get install - < requirements.txt
  exit 1;
elif [[ ! -z $APT ]]; then
  apt update
  apt install - < requirements.txt
elif [[ ! -z $DNF ]]; then
  dnf check-update
  dnf install - < requirements.txt
  exit 1;
elif [[ ! -z $PKG ]]; then
  pkg update
  pkg install - < requirements.txt
  exit 1;
elif [[ ! -z $PACMAN ]]; then
  pacman -Syu  
  pacman -S - < requirements.txt
  exit 1;
elif [[ ! -z $MAKE ]]; then
  make update
  make install - < requirements.txt
  exit 1;
else
  echo "Cannot install the packages! Try to install them manually."
  exit 1;
fi
