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
    docker rmi $(docker images --format {{.Repository}}:{{.Tag}} andi91/$name)
    docker build --no-cache --pull --progress=plain -t andi91/$name $name
    if [ -z $(docker images -q andi91/$name) ]
    then
    	builderror="$builderror $name %0A"
    	echo "$builderror"
    else
		docker image tag andi91/$name:latest andi91/$name:$todaydate
		docker push andi91/$name:latest
		docker push andi91/$name:$todaydate
	fi
done

if [ ! -z "$builderror" ]
then
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger&text=Docker-Builder Error:$builderror"
else
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger&text=Docker-Builder: %0AAll Fine"
fi