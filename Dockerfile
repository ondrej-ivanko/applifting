FROM python:3.7.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /applifting/

ENV DEBUG False

WORKDIR /applifting

RUN apt-get update && \
    apt-get install -y git && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x  get_offers_token.sh && \
    apt-get purge -y git && \
    apt-get autoremove -y && \
    apt-get clean

EXPOSE 8080
