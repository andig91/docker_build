FROM debian:latest
#FROM ubuntu:latest #ausprobieren

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip && \
    pip3 install cloudscraper --break-system-packages
#https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-manag

ENTRYPOINT []
CMD ["bash"]
