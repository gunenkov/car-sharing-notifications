FROM python:3.11.2-slim-buster

WORKDIR /app

RUN pip3 install pika pytelegrambotapi python-dotenv --no-cache-dir

COPY . .

CMD ["python3", "main.py"]
