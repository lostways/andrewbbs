# Build Stage
FROM python:3.10-alpine as build-stage

# Install required system dependencies
RUN apk update && apk add \
    build-base \
    linux-headers \
    libpq-dev \
    pcre-dev \
    python3-dev

# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1

# Flushing out python buffer
ENV PYTHONUNBUFFERED 1

# Install uwsgi
RUN pip wheel --wheel-dir /usr/src/app/wheels uwsgi

# Install pip requirements
COPY ./app/requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip install --upgrade pip && pip wheel --wheel-dir /usr/src/app/wheels  \
    -r requirements.txt

# Run Stage
FROM python:3.10-alpine

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Install required system dependencies
RUN apk update && apk add \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # uWSGI dependencies
    pcre-dev \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from build stage
COPY --from=build-stage /usr/src/app/wheels /wheels/

# Install Python Dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    # Cleaning up unused files
    && rm -rf /wheels/

# COPY app files
COPY ./app/ .

# Copy entrypoint
COPY ./docker/production/django/entrypoint.sh .

# Copy uwsgi config
COPY ./docker/production/django/uwsgi.ini .

# Entry point
ENTRYPOINT [ "/app/entrypoint.sh" ]

# Start uWSGI
CMD [ "uwsgi", "--ini", "/app/uwsgi.ini" ]
