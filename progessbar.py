import boto3

info = []
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))
access_id = info[0]
access_secret = info[1]

user = '3'
fileID = 'test.mp4'
upload_sqs_url = "https://sqs.us-west-2.amazonaws.com/748786065780/DISSECT-FILE-PROGRESS_{}_{}".format(user,fileID)

sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id=access_id, \
                    aws_secret_access_key=access_secret)
progress= sqs.Queue(upload_sqs_url)
percent = 0
while percent != 100:
    messages=progress.receive_messages(MaxNumberOfMessages=1,WaitTimeSeconds=0,MessageAttributeNames=['All'])
    for message in messages:
        try:
            temp = int(message.message_attributes.get('percentDone').get('StringValue'))
        except:
            continue
        else:
            percent = temp
            print "{}%".format(percent)
            message.delete()


