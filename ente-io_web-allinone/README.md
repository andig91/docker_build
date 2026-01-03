# Image on Docker Hub  
## andi91/ente-io_web-allinone

***UPDATE 2026: Image build deactivated***
***Now there is a pre-built-image from the ente.io: https://github.com/ente-io/ente/blob/main/web/docs/docker.md***  

***DISCLAIMER: I never really test the allinone-image, because I personally use only the auth-app, but build succeed every week without errors***  

A docker image for 2FA-Auth-Web-Frontend/App from [ente-io](https://ente.io/).  
Works with the Backend-Server from ente-io `ghcr.io/ente-io/server`.  
There was no docker image for the docker-frontends, but a Dockerfile in the docs:  
https://help.ente.io/self-hosting/guides/web-app  
https://github.com/ente-io/ente/discussions/3778  

So there now three docker images:  
- all-in-one-frontend: andi91/ente-io_web-allinone von https://github.com/andig91/docker_build/tree/main/ente-io_web-allinone
- auth-App: andi91/ente-io_web-auth von https://github.com/andig91/docker_build/tree/main/ente-io_web-auth
- photos-App: andi91/ente-io_web-photos von https://github.com/andig91/docker_build/tree/main/ente-io_web-photos

Multiarch build not working, so only amd64. 