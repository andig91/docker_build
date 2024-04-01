FROM kasmweb/core-debian-bookworm:1.15.0
USER root

ENV HOME /home/kasm-default-profile
ENV STARTUPDIR /dockerstartup
ENV INST_SCRIPTS $STARTUPDIR/install
WORKDIR $HOME

######### Customize Container Here ###########

RUN apt update && \
curl https:$(curl https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html | grep "icaclient_" | grep "amd64.deb" | awk -F'rel="' '{print $2}' | cut -d "\"" -f 1) -o /tmp/icaclient_amd64.deb

RUN DEBIAN_FRONTEND="noninteractive" && \ 
#RUN debconf-set-selections <<< "icaclient app_protection/install_app_protection select yes" 
echo "icaclient app_protection/install_app_protection select yes" | debconf-set-selections && \ 
debconf-show icaclient && \ 
apt install -yq -f /tmp/icaclient_amd64.deb 

RUN apt-get install -y --no-install-recommends \
    chromium \
    chromium-l10n


######### End Customizations ###########

RUN chown 1000:0 $HOME
RUN $STARTUPDIR/set_user_permission.sh $HOME

ENV HOME /home/kasm-user
WORKDIR $HOME
RUN mkdir -p $HOME && chown -R 1000:0 $HOME

USER 1000