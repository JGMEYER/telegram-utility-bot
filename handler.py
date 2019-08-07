import json
import logging
import os
import re
import sys
from typing import Dict

from streaming import SUPPORTED_STREAMING_SERVICES, get_streaming_service_for_url

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

def urls_in_message(msg):
    urls = [w for w in msg.split(' ') if re.match('http[s]?://.*', w)]
    return urls

def handle_streaming_urls(msg):
    urls = urls_in_message(msg)
    if not urls:
        return
    for url in urls:
        logging.info("URL detected")
        logging.info(url)
        svc = get_streaming_service_for_url(url)
        if svc:
            similar_urls = get_similar_urls_for_streaming_url(svc, url)
        else:
            logging.info("URL is not for a supported streaming service")
            return
    print(similar_urls)

def get_similar_urls_for_streaming_url(url_svc, url):
    """Returns dict of urls from other streaming services for the same track"""
    trackId = url_svc.get_trackId_from_url(url)
    with url_svc() as svc_client:
        original_track = svc_client.get_track_from_trackId(trackId)

    similar_urls: Dict[str, str] = {}
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc is url_svc:
            continue
        with svc() as svc_client:
            try:
                track = svc_client.search_one_track(original_track.searchable_name)
                similar_urls[svc.__name__] = track.share_link() if track else "No result"
            except:
                logging.error("Getting track from trackId", exc_info=True)
    return similar_urls


if __name__ == '__main__':
    handle_streaming_urls('https://open.spotify.com/track/6VhFUajcI7aVBDe07R8Her?si=DmArdMdATQ-OVdhiJGKKBw')
    handle_streaming_urls('https://youtu.be/olgaAUJzAu4')
