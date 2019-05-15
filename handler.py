import json
import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

BOPIZ_CHAT_ID = -1001163985660  # Stream Team
ALERT_CHAT_ID = BOPIZ_CHAT_ID
ALERT_GROUP = {
  'Knallharter',
  'Zimexerz',
  'AlexWOT',
  'TheRam254',
  'Dragonnuggets',
}

def handler(event, context):
    """
    Perform appropriate action for each endpoint invocation
    """
    if event['path'] == "/telegram/alert":
        return send_alert(event, context)
    elif event['path'] == "/telegram/musicConverter":
        return {"statusCode": 400}  # not yet available
    return {"statusCode": 400}

#TODO GENERALIZE CODE DETAILS
def send_alert(event, context):
    try:
        event_body = json.loads(event['body'])
        alerter = event_body['alerter']
    except Exception as e:
        logging.error("Processing alert request body", exc_info=True)
        return {"statusCode": 400}

    try:
        mentions = [f"@{u}" for u in ALERT_GROUP if u != alerter]
        response = (
            f":: BOPIZ ALERT ::\n"
            f"{alerter} Needs your help!\n"
            f"\n"
            f"{', '.join(mentions)}")

        data = {"text": response.encode("utf8"), "chat_id": ALERT_CHAT_ID}
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
