#!/bin/bash

todaydate=$(date +%F)

if [ -z "$1" ]
then
	echo "Bitte Build-Ordner angeben"
	exit
fi

if [ -z "$2" ]
then
	echo "Push to Docker-Registry and $(sed -n 5p cred.txt)"
else
	echo "Push only to $(sed -n 5p cred.txt)"
fi

if [ -d $1 ]; then
	echo "Dir exists"
    name=$(echo "$d" | cut -d "/" -f 1)
	docker build --no-cache --pull --progress=plain -t $(sed -n 5p cred.txt)/andi91/$1 $1
	docker image tag $(sed -n 5p cred.txt)/andi91/$1:latest $(sed -n 5p cred.txt)/andi91/$1:$todaydate
	docker push $(sed -n 5p cred.txt)/andi91/$1:latest
	docker push $(sed -n 5p cred.txt)/andi91/$1:$todaydate
	if [ -z "$2" ]
	then
		docker image tag $(sed -n 5p cred.txt)/andi91/$1:latest andi91/$1:latest
		docker image tag $(sed -n 5p cred.txt)/andi91/$1:latest andi91/$1:$todaydate
		docker push andi91/$1:latest
		docker push andi91/$1:$todaydate
	fi
else
	echo "Dir not existing"
fi

