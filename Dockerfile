ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY . /code

#COPY .env /code/.env

#RUN python manage.py migrate

RUN python manage.py createsuperuser --noinput; exit 0

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "student_behavior_tracker.wsgi"]
