FROM lscr.io/linuxserver/webtop:ubuntu-xfce

# Little Help
# https://www.linuxserver.io/blog/webtop-2-0-the-year-of-the-linux-desktop
# https://kasmweb.com/docs/latest/how_to/building_images.html
# https://github.com/linuxserver/docker-webtop/blob/ubuntu-xfce/Dockerfile
# https://github.com/kasmtech/workspaces-images/blob/develop/dockerfile-kasm-debian-bookworm-desktop  

#COPY /root2 /
# pip3 install cloudscraper replaced through apt install python3-cloudscraper
RUN \
  apt update &&\
  apt install -y wget python3 python3-pip &&\
  apt install python3-cloudscraper -y &&\
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - &&\
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list &&\
  apt update &&\
  apt install -y google-chrome-stable &&\
  sudo mkdir -p "/opt/google/chrome/extensions" &&\
  sudo bash -c 'echo "{" > "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"' &&\
  sudo bash -c 'echo "  \"external_update_url\": \"https://clients2.google.com/service/update2/crx\"" >> "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"' &&\
  sudo bash -c 'echo "}" >> "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"' &&\
  sudo echo Added \"/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json\" ["2Captcha Solver"]
  
# ports and volumes
EXPOSE 3000
EXPOSE 3389