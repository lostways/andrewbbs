FROM python:3.9 as app
EXPOSE 8000
WORKDIR /app
# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1
# Flushing out python buffer
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]