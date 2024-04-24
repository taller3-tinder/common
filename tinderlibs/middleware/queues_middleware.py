from dotenv import load_dotenv
import os
import boto3

load_dotenv()
MIDDLEWARE_HOST = os.getenv("MIDDLEWARE_HOST")  # Ex: http://localhost:4566
AWS_REGION = os.getenv("AWS_REGION")          # Ex: 'us-east-1'
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")  # Ex: 'dummy'
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")  # Ex: 'dummy'
QUEUE_NAME = os.getenv("QUEUE_NAME")  # Ex: my-queue
AWS_CLIENT = os.getenv("AWS_CLIENT")  # Ex: aws-localstack
TOPIC_PUBLISH = os.getenv("SNS_TOPIC")  # Ex: my-topic


class QueuesMiddleware:
    def __init__(self):
        self.aws_client = boto3.client(AWS_CLIENT,
                                       endpoint_url=MIDDLEWARE_HOST,
                                       region_name=AWS_REGION,
                                       aws_access_key_id=AWS_ACCESS_KEY,
                                       aws_secret_access_key=AWS_SECRET_KEY)
        self.listening = False
        if QUEUE_NAME:
            self.queue_url = self.__get_queue_url(QUEUE_NAME)

    def __get_queue_url(self, queue_name):
        return self.aws_client.get_queue_url(QueueName=queue_name)['QueueUrl']

    def start_receiving(self, callback):
        self.listening = True
        while (self.listening):
            messages = self.aws_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            if 'Messages' in messages:
                for message in messages['Messages']:
                    callback(message['Body'])
                    self.aws_client.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle'])

    def send(self, message):
        self.aws_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message
        )

    def publish(self, message):
        self.aws_client.publish(
            TopicArn=TOPIC_PUBLISH,
            Message=message
        )
