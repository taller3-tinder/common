import pika
import os
from dotenv import load_dotenv


load_dotenv()


class MiddlewareProd:
    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["MIDDLEWARE_HOST"]))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=os.environ["QUEUE_NAME"],
                                    durable=True)
        self._active_connection = True

    def start_receiving(self, callback):
        self._callback = callback
        self._channel.basic_consume(queue=os.environ["QUEUE_NAME"],
                                    on_message_callback=self.__callback)
        self._channel.start_consuming()

    def __callback(self, ch, method, properties, body):
        self._callback(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def stop(self):
        if not self._active_connection:
            raise Exception("Already Stopped")
        self._channel.stop_consuming()
        self._connection.close()
        self._active_connection = False
