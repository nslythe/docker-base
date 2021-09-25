ARG UBUNTU_VERSION=20.04

FROM ubuntu:${UBUNTU_VERSION}

ENV TZ=America/Montreal

RUN apt-get update && apt-get install -y python3 python3-pip tzdata

STOPSIGNAL SIGTERM

COPY root /

ENTRYPOINT ["python3", "-u", "/go.py"]
