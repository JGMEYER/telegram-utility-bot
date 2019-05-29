import json
import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_ALERT_GROUP = json.loads(os.environ['TELEGRAM_ALERT_GROUP'])

def handler(event, context):
    """Perform appropriate action for each endpoint invocation"""
    if event['path'] == "/telegram/alert":
        return telegram_alert(event, context)
    elif event['path'] == "/telegram/musicConverter":
        return {"statusCode": 400}  # not yet available
    return {"statusCode": 400}

def telegram_alert(event, context):
    try:
        event_body = json.loads(event['body'])
        alerter = event_body['alerter']
    except Exception as e:
        logging.error("Processing alert request body", exc_info=True)
        return {"statusCode": 400}

    try:
        mentions = [f"@{u}" for u in TELEGRAM_ALERT_GROUP if u != alerter]
        response = (
            f":: TEAM ALERT ::\n"
            f"{alerter} Needs your help!\n"
            f"\n"
            f"{', '.join(mentions)}")

        data = {"text": response.encode("utf8"), "chat_id": TELEGRAM_CHAT_ID}
        url = BASE_URL + "/sendMessage"
    except Exception as e:
        logging.error("Encoding message", exc_info=True)
        return {"statusCode": 500}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(response.content)
        logging.error("Sending telegram alert", exc_info=True)
        return {"statusCode": 500}
    except requests.exceptions.RequestException as e:
        logging.error("Sending telegram alert", exc_info=True)
        return {"statusCode": 500}

    return {"statusCode": 200}
