from abc import ABC, abstractmethod
import pika
import json
from dotenv import load_dotenv
import os

load_dotenv()
RABBIT_MQ_HOSTNAME = os.getenv("RABBIT_MQ_HOSTNAME")
RABBIT_MQ_USERNAME = os.getenv("RABBIT_MQ_USERNAME")
RABBIT_MQ_PASSWORD = os.getenv("RABBIT_MQ_PASSWORD")


class MessageBroker(ABC):
    @abstractmethod
    async def publish(self, message, event):
        pass


class RabbitMqBroker(MessageBroker):
    async def publish(self, message, event):
        credentials = pika.PlainCredentials(RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOSTNAME, port=5672, credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=event, exchange_type="fanout", durable=True)
        channel.queue_declare(queue=event, durable=True)
        channel.queue_bind(exchange=event, queue=event)
        channel.basic_publish(exchange=event, routing_key=event, body=json.dumps(dict(message)), properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
        connection.close()
