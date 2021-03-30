import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


## Slack Information 
SLACK_CHANNEL = os.environ['slackChannel']
HOOK_URL = os.environ["HOOK_URL"]


## Function Cloudwatch log
logger = logging.getLogger()
logger.setLevel(logging.INFO)


## main 
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    alarm_description = message['AlarmDescription']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    change_time = message['StateChangeTime']
        
    color = "#30db3f" if alarm_name.find("off") >= 0 else "#eb4034"
        
    slack_message = {
    "channel": SLACK_CHANNEL,
    "attachments": [{
        "color": color,
        "blocks": [
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*상태 변경 전:*\\n" + old_state
                },
                {
                    "type": "mrkdwn",
                    "text": "*상태 변경 후:*\\n" + new_state
                },
                {
                    "type": "mrkdwn",
                    "text": "*경보 이름:*\\n" + alarm_name
                },
                {
                    "type": "mrkdwn",
                    "text": "*경보 시간:*\\n" + change_time
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Cloud Watch :eyes:"
                },
                "style": "primary",
                "url": "<https://ap-northeast-2.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-2#dashboards:name=CPU>"
                }
            ]
        }
        ]
    }],
    "blocks": [
        {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":female_fairy: 놀랐니? 난 Knowre AWS 요정이야\\n*" + alarm_description + "* 이 되어서 알려주러 왔어!"
        }
        },
        {
        "type": "divider"
        },
        {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": reason
            }
        ]
        }
    ]
    }