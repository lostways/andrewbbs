FROM python:3.10-alpine


# Set the working directory
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN apk add \
    build-base \
    linux-headers \
    pcre-dev \
    python3-dev \
    postgresql-client \
    libpq-dev

# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1

# Flushing out python buffer
ENV PYTHONUNBUFFERED 1

# Install pip requirements
COPY requirements.txt .
RUN pip install uwsgi && \
    pip install --no-cache-dir -r requirements.txt

# COPY app files
COPY . .

# Create a group and user to run our app and become that user
ARG APP_USER=appuser
RUN addgroup -S ${APP_USER} && adduser -S ${APP_USER} -G ${APP_USER}
USER ${APP_USER}:${APP_USER}

# Entry point
ENTRYPOINT [ "/app/docker/production/django/entrypoint.sh" ]

# Start uWSGI
CMD [ "uwsgi", "--ini", "/app/docker/production/django/uwsgi.ini" ]
