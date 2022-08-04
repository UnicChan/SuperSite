FROM ubuntu

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5002
WORKDIR "/app"
CMD python3 /app/app.py
