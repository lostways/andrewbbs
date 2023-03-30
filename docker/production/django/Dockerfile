FROM python:3.10-alpine as app

# Set the working directory
RUN mkdir /app
WORKDIR /app
COPY . .

# Install dependencies
RUN apk add \
    build-base \
    linux-headers \
    pcre-dev \
    python3-dev \
    postgresql-client

# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1

# Flushing out python buffer
ENV PYTHONUNBUFFERED 1

# Install pip requirements
RUN pip install uwsgi && \
    pip install --no-cache-dir -r requirements.txt

# Entry point
ENTRYPOINT [ "/app/docker/production/django/entrypoint.sh" ]

# Start uWSGI
CMD [ "uwsgi", "--ini", "/app/docker/production/django/uwsgi.ini" ]