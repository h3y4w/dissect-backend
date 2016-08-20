import boto3
from filehandler import FileHandler
info = []
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))
access_id = info[0]
access_secret = info[1]
sqs_base_url = "https://sqs.us-west-2.amazonaws.com/748786065780/"
upload_sqs_url = "https://sqs.us-west-2.amazonaws.com/748786065780/SM-regularQueue"
download_sqs_url = ""
process_sqs_url = "https://sqs.us-west-2.amazonaws.com/748786065780/process-queue"

class DissectQueue (object):
    sqs = None
    downloadQueue = None
    uploadQueue = None
    processQueue = None

    def __init__(self):

        self.sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id=access_id, \
                    aws_secret_access_key=access_secret)

    def connectToQueues(self):
        self.uploadQueue = self.sqs.Queue(upload_sqs_url)
        #self.downloadQueue = self.sqs.Queue(download_sqs_url)
        self.processQueue = self.sqs.Queue(process_sqs_url)

    def checkUploadQueue(self):
        messages=self.uploadQueue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributeNames=['All'])
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

                success = self.processMessage(message,FILE,timeout=10)
                if success is True:
                    print 'DELETE MESSAGE HERE IT WAS SUCESSFUL'
                else:
                    print "HERE YOU HANDLE ERROR"

    def checkDownloadQueue(self):
        messages=self.downloadQueue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributesNames=['All'])
        for message in messages:
            pass
            #FILE['id'] = message.message_attributes.get('fileID').get('StringValue')


    def createUserQueue(self,FILE): #creates a temp queue for the user file information for web services
        FILE['id'] = FILE['id'].replace('.','')
        qname='DISSECT-FILE-PROGESS_{}_{}'.format(FILE['user'],FILE['id'])
        self.sqs.create_queue(
            QueueName=qname,
        )
        return sqs_base_url+qname

    def sendToUserQueue(self,FILE,percent): #send the progress to user queue which is then read by web services
        progressQueue = self.sqs.Queue(FILE['queue_url'])
        progressQueue.send_message(
            MessageBody='message',
            DelaySeconds=0,
            MessageAttributes={
                'percent': {
                    'StringValue': str(percent),
                    'DataType': 'String'
                }
            }
        )

    def processMessage(self,message,FILE,timeout=350):
        FILE['queue_url'] = self.createUserQueue(FILE)
        DFH = FileHandler(FILE)
        DFH.prepare()
        #for x in range(0,3):
            #try:
             #   message.change_visibility(VisibilityTimeout=timeout)
        DFH.process()
            #    return True

            #except Exception as e:
            #    print "ERROR: {}\n\n\n\n\n".format(e)
            #    DFH.reset()
        #print "ERROR THREE TIMES! PURGING FILES"
        #DFH.purge()
            #message.delete()





