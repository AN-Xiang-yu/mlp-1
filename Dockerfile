FROM python:3.10-slim

ADD requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR src

COPY main.py main.py


ENTRYPOINT ["python3", "main.py"]
