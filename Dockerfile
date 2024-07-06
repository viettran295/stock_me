FROM python:3.11-slim-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn -b 0.0.0.0:80 app:server