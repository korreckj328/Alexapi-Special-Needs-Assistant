#!/usr/bin/env python
import boto3
import os
import time

access_key ="YOUR_ACCESS_KEY"
access_secret ="YOUR_ACCCESS_SECRET"
region ="YOUR_REGION"
queue_url ="YOUR_QUEUE_URL"

def pop_message(client, url):
    response = client.receive_message(QueueUrl = url, MaxNumberOfMessages = 10)

    #last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
    return message
    
client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)

for i in range(0,10):
    try:
        message = pop_message(client, queue_url)
        print(message)

        if message == "off":
            os.system('aplay /home/pi/Alexapi-Special-Needs-Assistant/shutdown.wav')
            os.system('sudo shutdown -h now')

	elif message == "reboot":
	    os.system('aplay /home/pi/Alexapi-Special-Needs-Assistant/restarting.wav')
            os.system('sudo reboot')

        elif message == "vacation":
            os.system('aplay /home/pi/Alexapi-Special-Needs-Assistant/vacation.wav')
            os.system('crontab /home/pi/Alexapi-Special-Needs-Assistant/vacationcron.bak')

        elif message == "school":
            os.system('aplay /home/pi/Alexapi-Special-Needs-Assistant/school.wav')
            os.system('crontab /home/pi/Alexapi-Special-Needs-Assistant/schooldayscron.bak')
    except:
        pass
    time.sleep(5)
