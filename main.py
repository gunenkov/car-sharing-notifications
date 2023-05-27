import telebot
import os
import pika
from dotenv import load_dotenv

load_dotenv()

tg_token = os.environ["TG_TOKEN"]
tg_id = int(os.environ["TG_ID"])

rmq_host = os.environ["RMQ_HOST"]
rmq_port = int(os.environ["RMQ_PORT"])
rmq_username = os.environ["RMQ_USER"]
rmq_password = os.environ["RMQ_PASSWORD"]

bot = telebot.TeleBot(token=tg_token)

credentials = pika.PlainCredentials(rmq_username, rmq_password)
parameters = pika.ConnectionParameters(rmq_host, rmq_port, "/", credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue = "drives-notification"

channel.queue_declare(queue=queue)


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    bot.send_message(tg_id, text=body)


channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

print("Bot is ready!")
channel.start_consuming()
