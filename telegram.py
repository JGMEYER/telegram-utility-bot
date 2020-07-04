import logging
import requests
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def send_message(
    base_url, chat_id, text, parse_mode="markdown", disable_link_previews=False
):
    """Send message to telegram `chat_id`"""
    try:
        data = {
            "text": text.encode("utf8"),
            "chat_id": chat_id,
            "disable_web_page_preview": disable_link_previews,
            "parse_mode": parse_mode,
        }
    except Exception:
        log.error("Encoding Telegram message", exc_info=True)
        return {"statusCode": 500, "body": "Failed to encode Telegram message"}

    try:
        url = urljoin(base_url, "sendMessage")
    except Exception:
        log.error("Joining Telegram url")
        return {"statusCode": 500, "body": "Failed to join Telegram url"}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        log.error(response.content)
        log.error("Sending Telegram message", exc_info=True)
        return {
            "statusCode": 500,
            "body": "Failed to send Telegram message - HTTPError",
        }
    except requests.exceptions.RequestException:
        log.error("Sending Telegram message", exc_info=True)
        return {
            "statusCode": 500,
            "body": "Failed to send Telegram message - RequestException",
        }

    return {"statusCode": 200}
