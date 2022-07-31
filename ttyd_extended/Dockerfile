FROM andi91/curl_jq_alpine as loader
ARG TARGETARCH

RUN echo Das ist Loadiamge ${TARGETARCH} 
RUN if [[ $TARGETARCH == "arm64" ]]; then curl -sL https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.aarch64 -o /tmp/ttyd.arm64; fi && \
	if [[ $TARGETARCH == "arm" ]]; then curl -sL https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.armhf -o /tmp/ttyd.arm; fi && \
	if [[ $TARGETARCH == "amd64" ]]; then curl -sL https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.x86_64 -o /tmp/ttyd.amd64; fi

RUN if [[ $TARGETARCH == "amd64" ]]; then curl -sL https://github.com/krallin/tini/releases/download/v0.19.0/tini-amd64 -o /tmp/tini.amd64; fi && \
	if [[ $TARGETARCH == "arm" ]]; then curl -sL https://github.com/krallin/tini/releases/download/v0.19.0/tini-armhf -o /tmp/tini.arm; fi && \
	if [[ $TARGETARCH == "arm64" ]]; then curl -sL https://github.com/krallin/tini/releases/download/v0.19.0/tini-arm64 -o /tmp/tini.arm64; fi

RUN ls -1 /tmp

FROM ubuntu:20.04
ARG TARGETARCH

RUN echo Das ist Hauptiamge ${TARGETARCH} 

RUN apt-get update && apt-get install -y nano openssh-client screen

COPY --from=loader /tmp/ttyd.${TARGETARCH} /usr/bin/ttyd
RUN chmod +x /usr/bin/ttyd
#ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini-${TARGETARCH} /sbin/tini
COPY --from=loader /tmp/tini.${TARGETARCH} /sbin/tini
RUN chmod +x /sbin/tini

COPY setup_user_and_run.sh /root/setup_user_and_run.sh


EXPOSE 7681
WORKDIR /root

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["bash", "/root/setup_user_and_run.sh"]