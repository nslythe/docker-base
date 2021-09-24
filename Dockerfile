FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip

STOPSIGNAL SIGTERM

COPY root /



ENTRYPOINT ["python3", "-u", "/go.py"]
