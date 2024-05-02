from dotenv import load_dotenv
import os
import boto3

load_dotenv()
QUEUE_NAME = os.getenv("QUEUE_NAME")  # Ex: my-queue
TOPIC_PUBLISH = os.getenv("SNS_TOPIC")  # Ex: my-topic


class QueuesMiddleware:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        if TOPIC_PUBLISH:
            self.sns = boto3.client('sns')
        self.listening = False
        if QUEUE_NAME:
            self.queue_url = self.__get_queue_url(QUEUE_NAME)

    def __get_queue_url(self, queue_name):
        return self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

    def start_receiving(self, callback):
        self.listening = True
        while (self.listening):
            messages = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            if 'Messages' in messages:
                for message in messages['Messages']:
                    callback(message['Body'])
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle'])

    def stop(self):
        self.listening = False

    def send(self, message):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message
        )

    def publish(self, message):
        self.sns.publish(
            TopicArn=TOPIC_PUBLISH,
            Message=message
        )
