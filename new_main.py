import boto3
import requests
import os
import boto3conf
import time
os.environ['api_url'] = 'localhost:5000/'
class Manager(object):
    QH = None
    id = None
    region = None
    def __init__(self):
        id = 123
        self.QH = QueueHandler()
        heartbeat_url = self.QH.get_heartbeat_sqs()
        self.QH.add_queue(heartbeat_url, 'heartbeat')

    def spawn_worker(self):
       pass

    def terminate_worker(self):
       pass


    def check_heartbeat(self):
        alerts = self.QH.check_queue(heartbeat_queue=True)
        if alerts is not None:
            for alert in alerts:
                if alert.id == self.id or alert.id == 0:
                    if alert.body == 'Shutdown':
                        return False
                    elif alert.body == "Pause":
                        time.sleep(alert.pause_time)

                    elif alert.body == 'Update':
                        pass
                    return True


    def run(self, QH):
        self.heartbeat_sqs_url = self.QH.get_heartbeat_queue()
        while check_heartbeat():
            pass




class QueueHandler (object):
    heartbeat_queue = None
    sqs = None
    queues = {}
    def __init__(self, region):
        self.sqs = boto3.resource('sqs', region_name='us-west-2',
                                  aws_access_key_id=boto3conf.info[0], aws_secret_access_key=boto3conf.info[1])

    def get_heartbeat_queue(self, region):
        return requests.get(os.environ['api_url'] + 'manager/queue_url?region={}'.format(region)).json['queue_url']

    def create_user_queue(self):
        pass

    def add_queue(self, url, key):
        if key not in self.queues:
            self.queues[key] = self.sqs.Queue(url)

    def send_message(self, queue_name, message):
        response = self.queues['queue_name'].send_message(MessageBody=message['body'], DelaySeconds=0,
                                                          MessageAttributes=message['attributes'])
        return response

    def check_queue(self, sqs_name):
        return self.queues[sqs_name].receive_messages(MaxNumberOfMessages=10, MessageAttributeNames=['All'])


