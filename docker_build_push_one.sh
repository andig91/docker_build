#!/bin/bash

todaydate=$(date +%F)

if [ -z "$1" ]
then
	echo "Bitte Build-Ordner angeben"
	exit
fi

if [ -z "$2" ]
then
	echo "Push to Docker-Registry and registry.pu.gruber.tools"
else
	echo "Push only to registry.pu.gruber.tools"
fi

if [ -d $1 ]; then
	echo "Dir exists"
    name=$(echo "$d" | cut -d "/" -f 1)
	docker build --no-cache --pull --progress=plain -t registry.pu.gruber.tools/andi91/$1 $1
	docker image tag registry.pu.gruber.tools/andi91/$1:latest registry.pu.gruber.tools/andi91/$1:$todaydate
	docker push registry.pu.gruber.tools/andi91/$1:latest
	docker push registry.pu.gruber.tools/andi91/$1:$todaydate
	if [ -z "$2" ]
	then
		docker image tag registry.pu.gruber.tools/andi91/$1:latest andi91/$1:latest
		docker image tag registry.pu.gruber.tools/andi91/$1:latest andi91/$1:$todaydate
		docker push andi91/$1:latest
		docker push andi91/$1:$todaydate
	fi
else
	echo "Dir not existing"
fi

