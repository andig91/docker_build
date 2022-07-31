#!/bin/bash
echo userset starting

if [ -z "$user" ]
then
user=$(echo -n guest)
else
echo $user als Standard
fi

if [ -z "$password" ]
then
password=$(echo -n guest)
else
echo Passwort gesetzt
fi

useradd -m $user 
usermod -s /bin/bash $user 
usermod -s /bin/nologin root 
echo "$user:$password" | chpasswd
# Falls ich doch mal das Image anders aufbaue: https://askubuntu.com/questions/558669/renaming-user-name  
# clear user and password
user=$(echo -n secret)
password=$(echo -n secret)

echo start ttyd

/sbin/tini ttyd login
