FROM python:3.9

WORKDIR /app

COPY Pipfile* /app/
RUN pip install --no-cache-dir --upgrade pip pipenv && pipenv install --dev --system
RUN pip install psycopg2
COPY . /app/
