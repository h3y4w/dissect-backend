import boto3
import json
import boto3conf
import socket
import thread
import requests
import os

class ServiceManager(object):
    ec2 = None
    sqs = None
    snapshotId = None
    FILE = None
    queue = None
    dissectUserUrl='DISSECT_USER_QUEUE-{}_{}'
    sqs_base_url = "https://sqs.us-west-2.amazonaws.com/748786065780/"
    queue_url={'upload': "https://sqs.us-west-2.amazonaws.com/748786065780/SM-regularQueue",
               'download': None
               }

    queue_type = None

    def __init__ (self,queue_type):

        self.sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id=boto3conf.info[0],
                                  aws_secret_access_key=boto3conf.info[1])

        self.ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=boto3conf.info[0],
                                  aws_secret_access_key=boto3conf.info[1])
        self.snapshotId='ami-d732f0b7'

        self.queue_type = queue_type

    def run (self):
        self.connectToQueue()

        while True: #add some variable which request a rest api. if it says stop all services it turns to false
            if self.queue_type=='upload':
                self.checkUploadQueue()
                print "SUCCESSFULLY EXITED in run method"
                exit(0)
            else:
                'only queue type available currently is upload'
            print 'done faggot'

    def connectToQueue(self):
        self.queue = self.sqs.Queue(self.queue_url[self.queue_type])

    def launchInstance(self,FILE):
        address = '{}/workers/spawn'.format(os.environ['api_url'])
        r=requests.post(address,json=FILE)
        data=r.json()
        if data['Success'] is not None:
            self.pingInstance(data['Success']['Instance'],'9999')#MAKE FIRST PING MAKE SURE IT IS SUCCESSFULLY SETUP

    def pingInstance(self,instance_info,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(instance_info['dns'],port)
        sock.send('PING UNO')
        while True:
            data=sock.recv(1024)
            if data is not None:
                response=json.dumps(data)
                if response['Job']['Success'] is True:
                    requests.delete('{}/workers/{}/active'.format(os.environ['api_url'], instance_info['id']))

    def terminateInstance(self):
        pass

    def checkUploadQueue(self):
        messages=self.queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributeNames=['All'])
        for message in messages:
            FILE={}
            error = None
            try:
                error = 'aa'
                FILE['aa'] = message.message_attributes.get('accountAllocation').get('StringValue')

                error = 'id'
                FILE['id'] = message.message_attributes.get('fileID').get('StringValue') #turn int()

                error='name'
                FILE['name'] = message.message_attributes.get('fileName').get('StringValue')

                error = 'compress'
                FILE['compress'] = message.message_attributes.get('fileCompress').get('StringValue')

                error = "ratio"
                FILE['ratio'] = 3 # ADD OPTION IN QUEUE

                error = 'user'
                FILE['user_id'] = message.message_attributes.get('user').get('StringValue')


                FILE['sizeGB'] = 5 #MAKE SURE TO ADD GB SIZE INDEX FOR INSTANCE CREATION
            except Exception as e:
                print str(e)
                print 'Message attribute: '
                print 'ERROR @ {}'.format(error)

            else:
                print 'Account Allocation=' + FILE['aa']
                print 'File ID=' + FILE['id']
                print 'FILE name=' + FILE['name']
                print 'file compress=' + FILE['compress']
                self.launchInstance(FILE)


    def sendInstanceDNS(self, DNS):
        progressQueue = self.sqs.Queue(self.FILE['queue_url'])
        progressQueue.send_message(
            MessageBody='VM INFO',
            DelaySeconds=0,
            MessageAttributes={
                'DNS': {
                    'StringValue': DNS,
                    'DataType': 'String'
                }
            }
        )



app = ServiceManager('upload') #change to os.environ['manager_type']
app.run()
#thread.start_new_thread(app.run,())


