#!/bin/bash

cd "$(dirname -- "$0")"
pwd -P

if [ -f "cred.txt" ]
then
	token=$(sed -n 1p cred.txt)
	empfanger=$(sed -n 2p cred.txt)
fi

if [[ $(ls -1A */multiarch) ]]
then
	echo "Multiarch builds exists"
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker buildx create --name mybuilder
	docker buildx use mybuilder
fi

builderror=""

todaydate=$(date +%F)

for d in */ ; do
    name=$(echo "$d" | cut -d "/" -f 1)
    echo
    echo
    echo "Build starting $name"
    #ls -la */*
    #sleep 3
    if [ -f "$name/multiarch" ]
	then
		architecture=$(sed -n 1p $name/multiarch)
		echo $architecture
		docker buildx build --platform $architecture -t andi91/$name:latest --push --no-cache $name
    	docker buildx build --platform $architecture -t andi91/$name:$todaydate --push $name
    	if $(docker manifest inspect andi91/$name:$todaydate 2>&1 | grep -qc "no such manifest")
    	then
    		builderror="$builderror $name %0A"
			echo "$builderror"
		fi
	else
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
	fi
done

docker buildx stop mybuilder
docker buildx rm mybuilder

if [ ! -z "$builderror" ]
then
	echo "Docker-Builder Error:$builderror"
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger" -d text="Docker-Builder Error: %0A$builderror"
else
	echo "Docker-Builder: All Fine"
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger" -d text="text=Docker-Builder: %0AAll Fine"
fi




