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

BOPIZ_TEST_CHAT_ID = -205156447  # ENS Bot Test Group
BOPIZ_CHAT_ID = -1001163985660  # Stream Team
ALERT_CHAT_ID = BOPIZ_CHAT_ID
ALERT_GROUP = {
  'Knallharter',
  'Zimexerz',
  'AlexWOT',
  'TheRam254',
  'Dragonnuggets',
}

#TODO GENERALIZE CODE DETAILS
#TODO FIX ENDPOINT NAMES
def hello(event, context):
    http_status_code = send_alert(event, context)
    return {"statusCode": http_status_code}

def send_alert(event, context):
    try:
        event_body = json.loads(event['body'])
        alerter = event_body['alerter']
    except Exception as e:
        logging.error("Processing alert request body", exc_info=True)
        return 400

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
        return 500

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(response.content)
        logging.error("Sending telegram alert", exc_info=True)
        return 500
    except requests.exceptions.RequestException as e:
        logging.error("Sending telegram alert", exc_info=True)
        return 500

    return 200
