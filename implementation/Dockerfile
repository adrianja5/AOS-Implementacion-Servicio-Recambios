FROM python:3.9-alpine

WORKDIR /service

COPY app /service/app/
COPY requirements.txt /service/requirements.txt

RUN apk add --no-cache build-base && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    apk del --purge build-base && \
    mkdir -p /service/db

EXPOSE 8080

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080
