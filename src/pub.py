import pika
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()
amqp_url=os.environ.get("RABBIT_MQ_URL")
amqp_queue_name=os.environ.get("RABBIT_MQ_QUEUE_NAME")
# Parse the URI
url_parameters = pika.URLParameters(amqp_url)

# Establish connection
connection = pika.BlockingConnection(url_parameters)

channel = connection.channel()

channel.queue_declare(queue=amqp_queue_name)

message = "b60d8c0c-07f4-48a5-a159-11a9c303e377"

channel.basic_publish(exchange='', routing_key=amqp_queue_name, body=message)

print(f"sent message: {message}")

channel.close()
  