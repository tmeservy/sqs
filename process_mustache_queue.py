import boto3
import botocore
import json
import mustache
import time
import os
import shutil

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='mustache')

while True:
    #get the next message from the queue
    messages = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=5)

    #check the number of messages; sleep if there aren't any
    print("Num Messages: {0}".format(len(messages)))
    if (len(messages)==0):
        time.sleep(60)
        continue 

    #process messages if there are some
    print("continuing to process messages because at least one was found")	
    for message in messages:
        # parse the message body for the bucketname and filename
        parsedmessage = json.loads(message.body)	
        bucket = parsedmessage["Records"][0]["s3"]["bucket"]["name"]
        filename = parsedmessage["Records"][0]["s3"]["object"]["key"]

        #setup s3 object and download file
        s3 = boto3.resource('s3')
        downloadfilepath = "./temp/"+filename
        os.mkdir("./temp/")

        try:
            s3.Bucket(bucket).download_file(filename, downloadfilepath)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        #now add the mustache to the image that was downloaded
        print("Working on "+downloadfilepath)
        addedimage = mustache.add_mustache(downloadfilepath)
        print("New image: "+addedimage)

        #now upload the image to s3
        uploadbucket = "tmeservy-withmustaches"
        s3_client = boto3.client('s3')
        s3_client.upload_file(addedimage, uploadbucket, addedimage.replace("./temp/",""))
        print("File uploaded to S3")


        message.delete()

        #clean up the files that were processed
        shutil.rmtree('./temp/')
