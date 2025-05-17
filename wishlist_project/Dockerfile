FROM python:3.12

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY celery_tasks/start_celery.sh /app/celery_tasks/start_celery.sh
COPY celery_tasks/start_celery_beat.sh /app/celery_tasks/start_celery_beat.sh
RUN chmod +x /app/celery_tasks/start_celery.sh
RUN chmod +x /app/celery_tasks/start_celery_beat.sh

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000
