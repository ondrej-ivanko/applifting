FROM python:3.7.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /applifting/

ENV DEBUG False

WORKDIR /applifting

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y mawk 1.3.4 && \
    apt-get install -y git && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x  bash_get_token.sh && \
    apt-get purge -y git && \
    apt-get autoremove -y && \
    apt-get clean && \
    ./bash_get_token.sh

EXPOSE 8080

ENTRYPOINT [ "gunicorn" ]

CMD [ "applifting.wsgi", "--bind", "0.0.0.0:8080", "--workers", "5" ]