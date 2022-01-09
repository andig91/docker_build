#!/bin/bash

install_chrome_extension () {
  #preferences_dir_path="/config/.config/google-chrome/Default/Extensions/"
  preferences_dir_path="/opt/google/chrome/extensions"
  pref_file_path="$preferences_dir_path/$1.json"
  upd_url="https://clients2.google.com/service/update2/crx"
  mkdir -p "$preferences_dir_path"
  echo "{" > "$pref_file_path"
  echo "  \"external_update_url\": \"$upd_url\"" >> "$pref_file_path"
  echo "}" >> "$pref_file_path"
  echo Added \""$pref_file_path"\" ["$2"]
}

if ! which "google-chrome" ; then
  sudo apt-get update
  sudo apt-get install wget
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
  sudo apt-get update
  sudo apt install google-chrome-stable
else
  echo Chrome already installed
fi

#mkdir /config/.config/google-chrome/
#touch "/config/.config/google-chrome/First Run"
#google-chrome --load-extension=2Captcha-Solver_v1.6.6

install_chrome_extension "ifibfemgeogfhoebkmokieepdoobkbpo" "2Captcha Solver"
#install_chrome_extension "fmkadmapgofadopljbjfkapdkoienihi" "react dev tools"
#install_chrome_extension "anmidgajdonkgmmilbccfefkfieajakd" "save pinned tabs"
#install_chrome_extension "dbepggeogbaibhgnhhndojpepiihcmeb" "vimium"
