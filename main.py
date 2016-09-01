import boto3
import json

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

        self.sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id=access_id,
                                  aws_secret_access_key=access_secret)

        self.ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=access_id,
                                  aws_secret_access_key=access_secret)
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

    def launchInstance(self):
        string_json = json.dumps(self.FILE)
        print string_json

        self.createUserQueue()
        with open('prepare.sh') as prepare_file:
            UserData=prepare_file.read() % string_json
        instance = self.ec2.create_instances(ImageId=self.snapshotId,
                                        MinCount=1,
                                        MaxCount=1,
                                        SecurityGroupIds=[
                                            'sg-b2ba5fcb',
                                        ],
                                        UserData=UserData,
                                        InstanceType='t2.micro',
                                        KeyName='heyaws',
                                        BlockDeviceMappings=[
                                            {
                                                'DeviceName': '/dev/sdb',
                                                'Ebs': {
                                                    'VolumeSize': self.FILE['sizeGB'],
                                                    'DeleteOnTermination': True,
                                                    'VolumeType': 'gp2', #'Iops': 123, NOT SUPPORTED FOR gp2
                                                    'Encrypted': False
                                                },
                                            },
                                        ]
                                        )[0]

        instance.wait_until_running()
        instance.load()
        self.sendInstanceDNS(instance.public_dns_name)
        print instance.public_dns_name
        print "DONE"

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
                FILE['user'] = message.message_attributes.get('user').get('StringValue')


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
                self.FILE = FILE
                self.launchInstance()


    def createUserQueue(self): #creates a temp queue for the user file information for web services
        qname=self.dissectUserUrl.format(self.FILE['user'],self.FILE['id'])
        self.sqs.create_queue(
            QueueName=qname,
        )
        self.FILE['queue_url']=self.sqs_base_url+qname

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


info=[]
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))
access_id = info[0]
access_secret = info[1]

app = ServiceManager('upload')
app.run()


