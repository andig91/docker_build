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
	logfile=/tmp/buildlog_$name.txt
	echo
	echo
	echo "Build starting $name"
	#ls -la */*
	#sleep 3
	# Clear Builderror on each iteration
	builderror_local=""
	if [ -f "$name/multiarch" ]
	then
		architecture=$(sed -n 1p $name/multiarch)
		echo $architecture
		echo "$name $architecture" > $logfile
		docker buildx build --platform $architecture -t andi91/$name:latest --push --no-cache $name >> $logfile 2>&1
		docker buildx build --platform $architecture -t andi91/$name:$todaydate --push $name >> $logfile 2>&1
		if $(docker manifest inspect andi91/$name:$todaydate 2>&1 | grep -qc "no such manifest")
		then
			builderror_local="$name"
			echo "$builderror_local"
		fi
	else
		echo "$name singlearch" > $logfile
		docker rmi $(docker images --format {{.Repository}}:{{.Tag}} andi91/$name) >> $logfile 2>&1
		docker build --no-cache --pull --progress=plain -t andi91/$name $name >> $logfile 2>&1
		if [ -z $(docker images -q andi91/$name) ]
		then
			builderror_local="$name"
			echo "$builderror_local"
		else
			docker image tag andi91/$name:latest andi91/$name:$todaydate >> $logfile 2>&1
			docker push andi91/$name:latest >> $logfile 2>&1
			docker push andi91/$name:$todaydate >> $logfile 2>&1
		fi
	fi
	# Send complete buildlog, if variable is filled  
	if [ -n "$builderror_local" ]
	then
		builderror="$builderror $name %0A"
		stringlengh=$(wc -c $logfile | cut -d " " -f 1)
		echo $stringlengh
		if [ $stringlengh -gt 65000 ]
		then
			split -b 65000 --numeric-suffixes $logfile /tmp/buildlog_splitted_
			datalog="["
			for splitfile in /tmp/buildlog_splitted_*
			do
				echo $splitfile 
				datalog="$datalog"'{
					"image": "'Testing'",
					"success": 0,
					"log": '"$(cat $splitfile | jq -Rsa)"'
				},'
			done
			datalog=$(echo "$datalog" | sed '$s/,/]/')
			#datalog2="echo ${datalog/%.0/.X}"
			rm /tmp/buildlog_splitted_*
		else
			datalog='{
					"image": "'Testing'",
					"success": 0,
					"log": '"$(cat $logfile | jq -Rsa)"'
				}'
		fi

		curl --location 'http://'$(sed -n 4p cred.txt)'/items/Docker_Build?access_token='$(sed -n 3p cred.txt)'' \
			--header 'Content-Type: application/json' \
			--data "$datalog"
	#		--data '{
	#			"image": "'$name'",
	#			"success": 0,
	#			"log": '"$(cat $logfile | jq -Rsa)"'
	#		}'
	else
		curl --location 'http://'$(sed -n 4p cred.txt)'/items/Docker_Build?access_token='$(sed -n 3p cred.txt)'' \
		--header 'Content-Type: application/json' \
		--data '{
			"image": "'$name'",
			"success": 1,
			"log": "All Fine!"
		}'
	fi
done

docker buildx stop mybuilder
docker buildx rm mybuilder

# Send complete buildlog, if variable is filled. Double negative  
if [ ! -z "$builderror" ]
then
	echo "Docker-Builder Error:$builderror"
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger" -d text="Docker-Builder Error: %0A$builderror"
else
	echo "Docker-Builder: All Fine"
	curl "https://api.telegram.org/bot$token/sendMessage?chat_id=$empfanger" -d text="Docker-Builder: %0AAll Fine"
fi

docker rmi $(docker images -aq)
docker builder prune -af

