import datetime
import json
import logging
import os
import requests

from streaming.match import get_mirror_links_message, urls_in_text

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def getenv(env):
    """HACK use dev for running local unit/integration tests"""
    try:
        return os.environ[env]
    except KeyError:
        logging.warning(f"{env} missing, defaulting to {env}_DEV")
        return os.environ[env + "_DEV"]


TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
BASE_URL = "https://api.telegram.org/bot{}".format(TELEGRAM_TOKEN)

TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")
TELEGRAM_ALERT_GROUP = json.loads(os.environ["TELEGRAM_ALERT_GROUP"])


def handler(event, context):
    """Perform appropriate action for each endpoint invocation"""
    try:
        if event["path"] == "/hello":
            return {"statusCode": 200, "body": "hello, world!"}
        elif event["path"] == "/alert":
            return send_alert(event, context)
        elif event["path"] == "/webhookUpdate":
            return handle_webhook_update(event, context)
    except Exception:
        logging.error("Handling request", exc_info=True)
        return {"statusCode": 500}
    return {"statusCode": 404}


"""
Endpoint Handlers
"""


def send_alert(event, context):
    try:
        event_body = json.loads(event["body"])
        alerter = event_body["alerter"]
    except Exception:
        logging.error("Processing alert request body", exc_info=True)
        return {"statusCode": 400}

    mentions = [f"@{u}" for u in TELEGRAM_ALERT_GROUP if u != alerter]
    response = (
        f":: TEAM ALERT ::\n"
        f"{alerter} Needs your help!\n"
        f"\n"
        f"{', '.join(mentions)}"
    )
    return send_message(response, TELEGRAM_CHAT_ID)


def handle_webhook_update(event, context):
    event_body = json.loads(event["body"])

    # message edits intentionally not supported for now
    if not event_body.get("message"):
        logging.info("Event is not a message (e.g. a message_edit). Ignore")
        return {"statusCode": 200}
    # ignore messages without text
    elif not event_body["message"].get("text"):
        logging.info("Event message contains no text (e.g. a sticker). Ignore")
        return {"statusCode": 200}

    try:
        msg_date = event_body["message"]["date"]
    except KeyError:
        logging.error("Parsing date from Telegram update", exc_info=True)
        return {"statusCode": 400}

    # avoid spamming our APIs
    timeout = 30  # seconds
    age = datetime.datetime.now().timestamp() - msg_date
    logging.info(f"Telegram update age: {age}s")
    if age > timeout:
        logging.info(f"Ignoring old Telegram update")
        return {"statusCode": 200}

    try:
        text = event_body["message"]["text"]
    except KeyError:
        logging.error("Parsing text from Telegram update", exc_info=True)
        return {"statusCode": 400}

    # handle music mirror links
    urls = urls_in_text(text)
    if urls:
        text = get_mirror_links_message(urls)
        if text:
            response = send_message(
                text, TELEGRAM_CHAT_ID, disable_link_previews=True
            )
            if response["statusCode"] != 200:
                return response

    return {"statusCode": 200}


"""
Helpers
"""


def send_message(text, chat_id, disable_link_previews=False):
    try:
        data = {
            "text": text.encode("utf8"),
            "chat_id": chat_id,
            "disable_web_page_preview": disable_link_previews,
            "parse_mode": "markdown",
        }
        url = BASE_URL + "/sendMessage"
    except Exception:
        logging.error("Encoding message", exc_info=True)
        return {"statusCode": 500}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.error(response.content)
        logging.error("Sending Telegram message", exc_info=True)
        return {"statusCode": 500}
    except requests.exceptions.RequestException:
        logging.error("Sending Telegram message", exc_info=True)
        return {"statusCode": 500}

    return {"statusCode": 200}
