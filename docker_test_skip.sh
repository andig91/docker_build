#!/bin/bash

cd "$(dirname -- "$0")"
pwd -P

if [ -f "cred.txt" ]
then
	token=$(sed -n 1p cred.txt)
	empfanger=$(sed -n 2p cred.txt)
fi

builderror=""

todaydate=$(date +%F)

for d in */ ; do
    name=$(echo "$d" | cut -d "/" -f 1)
    if [[ $name == _old__* ]];
	then
		echo "!!!Build skipped!!! $name"
		continue
	fi
	
	logfile=/tmp/buildlog_$name.txt
	echo
	echo
	echo "Build starting $name"

done


