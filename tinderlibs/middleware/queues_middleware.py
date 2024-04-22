from dotenv import load_dotenv
import os
import boto3

load_dotenv()
MIDDLEWARE_HOST = os.getenv("MIDDLEWARE_HOST")  # Ex: http://localhost:4566
AWS_REGION = os.getenv("AWS_REGION")          # Ex: 'us-east-1'
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")  # Ex: 'dummy'
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")  # Ex: 'dummy'


class QueuesMiddleware:
    def __init__(self):
        self.sqs = boto3.client('sqs', endpoint_url=MIDDLEWARE_HOST,
                                region_name=AWS_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_KEY)
        self.listening = False
        self.send_queue = None

    def __get_queue_url(self, queue_name):
        return self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

    def start_receiving(self, callback, queue_name=None):
        if not queue_name:
            queue_name = os.getenv("QUEUE_NAME")
        queue_url = self.__get_queue_url(queue_name)
        self.listening = True
        while (self.listening):
            messages = self.sqs.receive_message(QueueUrl=queue_url,
                                                MaxNumberOfMessages=10,
                                                WaitTimeSeconds=20)
            if 'Messages' in messages:
                for message in messages['Messages']:
                    callback(message['Body'])
                    self.sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle'])

    def send(self, message, queue_name=None):
        if not queue_name and not self.send_queue:
            self.send_queue = os.getenv("QUEUE_NAME")
        elif self.send_queue != queue_name or not self.send_queue:
            self.send_queue = queue_name
            self.queue_url = self.__get_queue_url(queue_name)
        self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=message)
