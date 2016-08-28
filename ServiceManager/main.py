import boto3

class ServiceManager(object):
    ec2 = None
    sqs = None
    snapshotId = None

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
        queue = self.connectToQueue()
        self.checkQueue(queue)

    def connectToQueue(self):
        return self.sqs.Queue(self.queue_url[self.queue_type])

    def launchInstance(self, FILE):
        FILE['sizeGB']=5

        with open('/home/deno/Programs/python/dissect-backend/services/prepare.sh') as prepare_file:
            UserData=prepare_file.read()
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
                                                    'VolumeSize': FILE['sizeGB'],
                                                    'DeleteOnTermination': True,
                                                    'VolumeType': 'gp2', #'Iops': 123, NOT SUPPORTED FOR gp2
                                                    'Encrypted': False
                                                },
                                            },
                                        ]
                                        )[0]

        instance.wait_until_running()
        instance.load()
        print(instance.public_dns_name)

    def terminateInstance(self):
        pass

    def checkQueue(self,queue):
        messages=queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributeNames=['All'])
        for message in messages:
            FILE={}
            error = None
            try:
                error = 'aa'
                FILE['aa'] = message.message_attributes.get('accountAllocation').get('StringValue')

                error = 'id'
                FILE['id'] = message.message_attributes.get('fileID').get('StringValue') #turn int()

                error = 'compress'
                FILE['compress'] = message.message_attributes.get('fileCompress').get('StringValue')

                error = "ratio"
                FILE['ratio'] = 3 # ADD OPTION IN QUEUE

                FILE['user'] = 3
                # ADD USER ID HERE
                error = "bucket"
                FILE['bucket'] = 'sm-uploaded-files'
            except Exception as e:
                print str(e)
                print 'Message attribute: '
                print 'ERROR @ {}'.format(error)

            else:
                print 'Account Allocation=' + FILE['aa']
                print 'File ID=' + FILE['id']
                print 'file compress=' + FILE['compress']

                success = self.processMessage(FILE)
                if success is True:
                    #message.delete()
                    print 'DELETE MESSAGE HERE IT WAS SUCESSFUL'
                else:
                    print "HERE YOU HANDLE ERROR"

    def processMessage(self,FILE):
        self.launchInstance(FILE)


info=[]
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))
access_id = info[0]
access_secret = info[1]

app = ServiceManager('upload')
FILE={}
app.launchInstance(FILE)

