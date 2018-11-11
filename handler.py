import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

BOPIZ_TEST_CHAT_ID = -205156447  # ENS Bot Test Group
BOPIZ_CHAT_ID = -265155578  # Stream Team

ALERT_CHAT_ID = BOPIZ_CHAT_ID

ALERT_GROUP = {
  'Knallharter',
  'Zimexerz',
  'AlexWOT',
  'TheRam254',
  'Dragonnuggets',
}

def hello(event, context):
    try:
        event_body = json.loads(event['body'])

        response = f"This is the old version -- get new instructions from Knall"

        alerter = event_body.get('alerter')
        if alerter:
            mentions = [f"@{u}" for u in ALERT_GROUP if u != alerter]
            response = (
                f":: BOPIZ ALERT ::\n"
                f"{alerter} Needs your help!\n"
                f"\n"
                f"{', '.join(mentions)}")

        data = {"text": response.encode("utf8"), "chat_id": ALERT_CHAT_ID}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
