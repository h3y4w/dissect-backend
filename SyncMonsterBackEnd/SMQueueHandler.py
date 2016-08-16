import boto3
from SMFileHandler import FileHandler
access_id = "AKIAI4MFBRLGFOROIF5A"
access_secret = "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"



upload_sqs_url = "https://sqs.us-west-2.amazonaws.com/748786065780/SM-regularQueue"
download_sqs_url = ""
process_sqs_url = "https://sqs.us-west-2.amazonaws.com/748786065780/process-queue"

class Queue (object):
    sqs = None
    downloadQueue = None
    uploadQueue = None
    processQueue = None

    def __init__(self):

        self.sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id=access_id, \
                    aws_secret_access_key=access_secret)

        self.uploadQueue = self.sqs.Queue(upload_sqs_url)
        #self.downloadQueue = self.sqs.Queue(download_sqs_url)
        self.processQueue = self.sqs.Queue(process_sqs_url)

    def checkUploadQueue(self):
        messages=self.uploadQueue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributeNames=['All'])
        for message in messages:
            FILE={}
            try:
                FILE['aa'] = message.message_attributes.get('accountAllocation').get('StringValue')
                FILE['id'] = message.message_attributes.get('fileID').get('StringValue') #turn int()
                FILE['compress'] = message.message_attributes.get('fileCompress').get('StringValue')
                FILE['ratio'] = 3 # ADD OPTION IN QUEUE
            except Exception as e:
                print str(e)
                print 'Message attribute: '
                print message.message_attributes


                if (int(raw_input('Delete Message anyway? '))==True):
                    message.delete()
            else:
                print 'Account Allocation=' + FILE['aa']
                print 'File ID=' + FILE['id']
                print 'file compress=' + FILE['compress']

                if (int(raw_input('Recieved Message! Delete?'))==True):
                    message.delete()

                self.processMessage(message,FILE,timeout=10)

    def checkDownloadQueue(self):
        messages=self.downloadQueue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10,MessageAttributesNames=['All'])
        for message in messages:
            pass
            #FILE['id'] = message.message_attributes.get('fileID').get('StringValue')


    def processMessage(self,message,FILE,timeout=350):
        message.change_visibility(VisibilityTimeout=timeout)
        SMFH = SMFileHandler(FILE)
        SMFH.process()
        #message.delete()
print "STARTING..."
SMQ = SMQueue()
while True:
    SMQ.checkUploadQueue()




