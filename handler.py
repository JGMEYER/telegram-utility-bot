import datetime
import json
import logging
import os

from streaming.match import get_mirror_links_message, urls_in_text
from utils import telegram
from utils.env import getenv
from utils.log import setup_logger

setup_logger(__name__)
log = logging.getLogger(__name__)

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
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
        log.error("Handling request", exc_info=True)
        return {
            "statusCode": 500,
            "body": "Failed to handle request, reason unknown",
        }
    return {"statusCode": 404, "body": f'{event["path"]} not found'}


"""
Endpoint Handlers
"""


def send_alert(event, context):
    try:
        event_body = json.loads(event["body"])
        alerter = event_body["alerter"]
    except Exception:
        log.error("Processing alert request body", exc_info=True)
        return {
            "statusCode": 400,
            "body": "Could not process alert from request body",
        }

    mentions = [f"@{u}" for u in TELEGRAM_ALERT_GROUP if u != alerter]
    response = (
        f":: TEAM ALERT ::\n"
        f"{alerter} Needs your help!\n"
        f"\n"
        f"{', '.join(mentions)}"
    )
    return telegram.send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, response)


def handle_webhook_update(event, context):
    event_body = json.loads(event["body"])

    # message edits intentionally not supported for now
    if not event_body.get("message"):
        log.info("Event is not a message (e.g. a message_edit). Ignore")
        return {"statusCode": 200, "body": "ok"}
    # ignore messages without text
    elif not event_body["message"].get("text"):
        log.info("Event message contains no text (e.g. a sticker). Ignore")
        return {"statusCode": 200, "body": "ok"}

    try:
        msg_date = event_body["message"]["date"]
    except KeyError:
        log.error("Parsing date from Telegram update", exc_info=True)
        return {
            "statusCode": 400,
            "body": "Could not parse date from Telegram update",
        }

    try:
        msg_chat_id = event_body["message"]["chat"]["id"]
    except KeyError:
        log.error("Parsing chat id from Telegram update", exc_info=True)
        return {
            "statusCode": 400,
            "body": "Could not parse chat id from Telegram update",
        }

    # avoid spamming our APIs
    timeout = 30  # seconds
    age = datetime.datetime.now().timestamp() - msg_date
    log.info(f"Telegram update age: {age}s")
    if age > timeout:
        log.info("Ignoring old Telegram update")
        return {"statusCode": 200, "body": "ok"}

    try:
        text = event_body["message"]["text"]
    except KeyError:
        log.error("Parsing text from Telegram update", exc_info=True)
        return {
            "statusCode": 400,
            "body": "Could not parse text from Telegram update",
        }

    # handle music mirror links
    urls = urls_in_text(text)
    if urls:
        response_text = get_mirror_links_message(urls)
        if text:
            response = telegram.send_message(
                TELEGRAM_TOKEN,
                msg_chat_id,
                response_text,
                disable_link_previews=True,
            )
            if response["statusCode"] != 200:
                return response

    return {"statusCode": 200, "body": "ok"}
