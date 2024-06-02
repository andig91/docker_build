# Image on Docker Hub  
## andi91/ente-io_web-auth  

A docker image for 2FA-Auth-Web-Frontend/App from [ente-io](https://ente.io/).  
Works with the Backend-Server from ente-io `ghcr.io/ente-io/server`.  
There was no docker image for the docker-frontends, but a Dockerfile in the Community:  
https://help.ente.io/self-hosting/guides/external-s3#_1-create-a-compose-yaml-file   

So there now two docker images:  
- auth-App: andi91/ente-io_web-auth von https://github.com/andig91/docker_build/tree/main/ente-io_web-auth
- photos-App: andi91/ente-io_web-photos von https://github.com/andig91/docker_build/tree/main/ente-io_web-photos

Multiarch build not working, so only amd64. 