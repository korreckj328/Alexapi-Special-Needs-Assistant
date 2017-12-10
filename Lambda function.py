import boto3

access_key = "YOUR ACCESS KEY"
access_secret = "YOUR ACCESS SECRET"
region ="us-east-1"
queue_url = "YOUR QUEUE URL"

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
    if intent_name == "PiOn":
        post_message(client, 'on', queue_url)
        message = "On"
    elif intent_name == "PiOff":
        post_message(client, 'off', queue_url)
        message = "off"
    elif intent_name == "PiReboot":
        post_message(client, 'reboot', queue_url)
        message = "reboot"
    else:
        message = "Unknown"
    
    speechlet = build_speechlet_response("Mirror Status", message, "", "true")
    return build_response({}, speechlet)
