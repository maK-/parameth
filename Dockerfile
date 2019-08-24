FROM python:2.7-slim

RUN apt update 
RUN apt upgrade -y
RUN apt install -y git gcc
RUN git clone https://github.com/maK-/parameth
WORKDIR parameth 
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "parameth.py"]
