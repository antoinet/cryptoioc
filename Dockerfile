FROM python:3.6

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV=prod
EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]