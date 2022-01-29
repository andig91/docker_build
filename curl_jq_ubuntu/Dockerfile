FROM debian:latest

RUN apt-get update && \
    apt-get install -y curl jq && \
    sed -i -e '$a--cipher '\''DEFAULT:!DH'\''' /etc/ssl/openssl.cnf

ENTRYPOINT ["/bin/bash"]
CMD []
