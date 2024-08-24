#!/bin/bash

todaydate=$(date +%F)

if [ -z "$1" ]
then
	echo "Bitte Build-Ordner angeben"
	exit
fi

if [ -z "$2" ]
then
	echo "Push to Docker-Registry and registry.gruber.live"
else
	echo "Push only to registry.gruber.live"
fi

if [ -f "$1/multiarch" ]
then
	architecture=$(sed -n 1p $1/multiarch)
	echo $architecture
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker buildx create --name mybuilder
	docker buildx use mybuilder
else
	echo "Kein Multiarch-File"
	exit
fi

#exit
if [ -d $1 ]; then
	echo "Dir exists"
    name=$(echo "$d" | cut -d "/" -f 1)
    docker buildx build  --platform $architecture -t registry.gruber.live/andi91/$1:latest --push --no-cache $1
    docker buildx build  --platform $architecture -t registry.gruber.live/andi91/$1:$todaydate --push $1
    if [ -z "$2" ]
	then
    	docker buildx build  --platform $architecture -t andi91/$1:latest --push $1
    	docker buildx build  --platform $architecture -t andi91/$1:$todaydate --push $1
	fi
	
	#docker build --no-cache --pull --progress=plain -t andi91/$1 $1
	#docker image tag andi91/$1:latest andi91/$1:$todaydate
	#docker push andi91/$1:latest
	#docker push andi91/$1:$todaydate
else
	echo "Dir not existing"
fi

docker buildx stop mybuilder
docker buildx rm mybuilder