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
    # Don't want to change the name of the folder
    # For me its better to create a file that controls that
    #if [[ $name == _old__* ]];
	if [ -f "$name/0_old_deprecated_noBuild" ]
	then
		echo
		echo
		echo "!!!Build skipped!!! $name"
		continue
	fi
	
	logfile=/tmp/buildlog_$name.txt
	echo
	echo
	echo "Build starting $name"

done


