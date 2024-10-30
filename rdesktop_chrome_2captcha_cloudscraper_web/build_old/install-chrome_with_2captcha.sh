#!/bin/bash

if ! which "google-chrome" ; then
  sudo apt-get update
  sudo apt-get install wget
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
  sudo apt-get update
  sudo apt install -y google-chrome-stable
else
  echo Chrome already installed
fi

mkdir /config/.config/google-chrome/
touch "/config/.config/google-chrome/First Run"


sudo mkdir -p "/opt/google/chrome/extensions"
sudo bash -c 'echo "{" > "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"'
sudo bash -c 'echo "  \"external_update_url\": \"https://clients2.google.com/service/update2/crx\"" >> "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"'
sudo bash -c 'echo "}" >> "/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json"'
sudo echo Added \"/opt/google/chrome/extensions/ifibfemgeogfhoebkmokieepdoobkbpo.json\" ["2Captcha Solver"]

#google-chrome 
#google-chrome-stable --remote-debugging-address=0.0.0.0 --remote-debugging-port=9228 &>/dev/null &
#google-chrome-stable --headless --remote-debugging-address=0.0.0.0 --remote-debugging-port=9228 &>/dev/null &

#install_chrome_extension "ifibfemgeogfhoebkmokieepdoobkbpo" "2Captcha Solver"
#install_chrome_extension "fmkadmapgofadopljbjfkapdkoienihi" "react dev tools"
#install_chrome_extension "anmidgajdonkgmmilbccfefkfieajakd" "save pinned tabs"
#install_chrome_extension "dbepggeogbaibhgnhhndojpepiihcmeb" "vimium"
