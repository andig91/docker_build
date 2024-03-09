FROM bash as builder
WORKDIR /src
RUN wget -O repo.tar.gz $(wget -O - https://api.github.com/repos/C0D3D3V/Moodle-DL/releases/latest | grep "tarball_url" | cut -d "\"" -f 4) && tar zxvf repo.tar.gz && mv C0D3D3V-Moodl* C0D3D3V-Moodle-DL


#FROM python:3.11
FROM python
COPY --from=builder /src/C0D3D3V-Moodle-DL /md

WORKDIR /md

RUN pip3 install .

ENTRYPOINT ["moodle-dl", "--path", "/files"]
