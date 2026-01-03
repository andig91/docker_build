FROM nodered/node-red:latest-debian
USER root
RUN apt-get install -y python3-pip python3-venv && mkdir /pyvenv && python3 -m venv /pyvenv && /pyvenv/bin/pip3 install requests playwright pyTelegramBotAPI tgtg
#RUN apk add py3-pip && mkdir /pyvenv && python3 -m venv /pyvenv
#RUN apk add py3-requests py3-pytest-playwright
#RUN apk add py3-pip
#RUN pip install requests playwright
USER node-red