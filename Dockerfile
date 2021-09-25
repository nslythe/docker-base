ARG UBUNTU_VERSION=20.04

FROM ubuntu:${UBUNTU_VERSION}

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=America/Montreal

RUN apt-get update && apt-get install -y python3 python3-pip tzdata
RUN python3 -m pip install requests

STOPSIGNAL SIGTERM

HEALTHCHECK CMD python3 -u /check_health.py

COPY root /

ENTRYPOINT ["python3", "-u", "/go.py"]
