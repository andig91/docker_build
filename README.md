# docker_build
Home for Dockerfiles and dependent Data
Support single- and multi-architecture builds



## Installation with buildx in a Proxmox-VM
Why VM? Doesn't work in (unprivileged) LXC....
Recommanded: https://pve.proxmox.com/wiki/Nested_Virtualization

### Install/Configure docker buildx
That helps me: https://vikaspogu.dev/posts/docker-buildx-setup/  

My steps:
```
#!/bin/bash


# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Login and clone git repo
sudo docker login
git clone https://github.com/andig91/docker_build.git
cd docker_build
vi cred.txt

# Test
sudo ./docker_build_push_one_multiarch.sh curl_jq_alpine

# Install crontab for weekly build and deploy on docker hub
sudo crontab -e
02 23 * * 6 /home/andig91/docker_build/docker_build_push_all.sh > /tmp/buildlog.txt
```
