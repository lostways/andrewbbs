FROM python:3.10 
EXPOSE 8000
WORKDIR /app

# copy app files
COPY ./app/ .

# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1
# Flushing out python buffer
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]