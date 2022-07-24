FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y curl jq  && \
    sed  -i '1i openssl_conf = default_conf' /etc/ssl/openssl.cnf && \
    echo "[ default_conf ]" >> /etc/ssl/openssl.cnf && \
	echo "" >> /etc/ssl/openssl.cnf && \
	echo "ssl_conf = ssl_sect" >> /etc/ssl/openssl.cnf && \
	echo "" >> /etc/ssl/openssl.cnf && \
	echo "[ssl_sect]" >> /etc/ssl/openssl.cnf && \
	echo "" >> /etc/ssl/openssl.cnf && \
	echo "system_default = system_default_sect" >> /etc/ssl/openssl.cnf && \
	echo "" >> /etc/ssl/openssl.cnf && \
	echo "[system_default_sect]" >> /etc/ssl/openssl.cnf && \
	echo "MinProtocol = TLSv1.2" >> /etc/ssl/openssl.cnf && \
	echo "CipherString = DEFAULT:@SECLEVEL=1' /etc/ssl/openssl.cnf" >> /etc/ssl/openssl.cnf
	#sed -i -e '$a--cipher '\''DEFAULT:!DH'\''' /etc/ssl/openssl.cnf

ENTRYPOINT []
CMD ["/bin/bash"]
