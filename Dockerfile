FROM python:3.11.8

RUN mkdir /backend

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x docker/*.sh