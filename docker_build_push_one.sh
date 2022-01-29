#!/bin/bash

todaydate=$(date +%F)

if [ -z "$1" ]
then
	echo "Bitte Build-Ordner angeben"
	exit
fi

if [ -d $1 ]; then
	echo "Dir exists"
    name=$(echo "$d" | cut -d "/" -f 1)
	docker build --no-cache --pull --progress=plain -t andi91/$1 $1
	docker image tag andi91/$1:latest andi91/$1:$todaydate
	docker push andi91/$1:latest
	docker push andi91/$1:$todaydate
else
	echo "Dir not existing"
fi

