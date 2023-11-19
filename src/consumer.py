import pika
import time
import random
import os
from dotenv import load_dotenv

from worker import send_log_to_supabase
def start_rabbitmq_consumer():
    load_dotenv()
    amqp_url=os.environ.get("RABBIT_MQ_URL")
    amqp_queue_name=os.environ.get("RABBIT_MQ_QUEUE_NAME")
    rabbitmq_prefetch_count=int(os.environ.get("RABBIT_MQ_PREFETCH_COUNT",10))
    def on_message_received(ch, method, properties, uid):
        send_log_to_supabase(uid)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # channel.stop_consuming()
    # Parse the URI
    url_parameters = pika.URLParameters(amqp_url)

    # Establish connection
    connection = pika.BlockingConnection(url_parameters)

    channel = connection.channel()

    channel.queue_declare(queue=amqp_queue_name)

    channel.basic_qos(prefetch_count=rabbitmq_prefetch_count)

    channel.basic_consume(queue=amqp_queue_name, on_message_callback=on_message_received)

    channel.start_consuming()
start_rabbitmq_consumer()