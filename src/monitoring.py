import requests
from requests.auth import HTTPBasicAuth

# RabbitMQ URL
rabbitmq_url = "amqps://uaesxxwq:UKT7QOcUwL0HCaSYzv-L9LG2j6j_VMqU@puffin.rmq2.cloudamqp.com/uaesxxwq"

# Parse RabbitMQ URL
url_parts = rabbitmq_url.split("//")[1].split(":")
username = url_parts[0]
password = url_parts[1].split("@")[0]
host = url_parts[1].split("@")[1].split("/")[0]

# RabbitMQ Management API URL
api_url = f"http://{host}:15672/api"

# Specify the queue name
queue_name = "your-queue-name"

# API endpoint for getting queue information
queue_info_url = f"{api_url}/queues/%2F/{queue_name}"

# Make a GET request to retrieve queue information
response = requests.get(queue_info_url, auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    queue_info = response.json()

    # Extract relevant information
    messages_ready = queue_info["messages_ready"]
    messages_unacknowledged = queue_info["messages_unacknowledged"]

    # Calculate the difference between production and consumption
    difference = messages_ready + messages_unacknowledged

    print(f"Messages Ready: {messages_ready}")
    print(f"Messages Unacknowledged: {messages_unacknowledged}")
    print(f"Difference: {difference}")
else:
    print(f"Error: {response.status_code}, {response.text}")
