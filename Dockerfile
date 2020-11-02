FROM python:3.8.5-alpine
LABEL MAINTAINER="Dan Streeter <dan@danstreeter.co.uk>"

RUN apk add --no-cache bash

# Install other required dependancies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy in code
COPY ./src /app

# Setup non root user
RUN adduser -D appuser && chown -R appuser: /app
USER appuser

WORKDIR /app

CMD gunicorn \
    --access-logfile - \
    --error-logfile - \
    --worker-tmp-dir /dev/shm \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --bind 0.0.0.0:8000 \
    main:create_app