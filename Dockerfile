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
    rm -rf /var/cache/apt/lists/*

RUN chmod u+x  bash_get_token.sh django-entrypoint.sh && \
    apt-get autoremove -y && \
    ./bash_get_token.sh

EXPOSE 8080

ENTRYPOINT ["/bin/bash"]

CMD [ "django-entrypoint.sh" ]
