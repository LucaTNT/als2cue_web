FROM tiangolo/meinheld-gunicorn-flask:python3.8-alpine3.11

COPY ./app /app
ENV PYTHONPATH /usr/lib/python3.8/site-packages
RUN apk add --no-cache py3-numpy py3-scipy git && pip3 install -r requirements.txt && apk del git
