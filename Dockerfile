FROM python:3.8.3-alpine3.12

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY .env .
ADD .env /code/

COPY requirements.txt .

ADD requirements.txt /code/
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt
ADD . /code/

COPY docker/initial-back.sh /docker-entrypoint.sh

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "loaddata", "inventory/fixtures/items_initial_data.json"]
CMD ["python", "manage.py", "shel", "-c", "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]