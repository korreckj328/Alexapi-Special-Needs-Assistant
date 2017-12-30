import boto3

access_key = "YOUR ACCESS KEY"
access_secret = "YOUR ACCESS SECRET"
region ="YOUR_REGION"
queue_url = "YOUR_QUEUE_URL"

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def post_message(client, message_body, url):
    response = client.send_message(QueueUrl = url, MessageBody= message_body)
    
def lambda_handler(event, context):
    client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)
    intent_name = event['request']['intent']['name']
    if intent_name == "PiOff":
        post_message(client, 'off', queue_url)
        message = "off"
    elif intent_name == "PiReboot":
        post_message(client, 'reboot', queue_url)
        message = "reboot"
    elif intent_name == "vacation":
        post_message(client, 'vacation', queue_url)
        message = "vacation"
    elif intent_name == "school":
        post_message(client, 'school', queue_url)
        message = "school"
    else:
        message = "Unknown"
        
    speechlet = build_speechlet_response("Pi Assistant", message, "", "true")
    return build_response({}, speechlet)
