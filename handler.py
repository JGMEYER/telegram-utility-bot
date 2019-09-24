import datetime
import json
import logging
import os
import re
import requests
from typing import Dict, List

from streaming import SUPPORTED_STREAMING_SERVICES, get_streaming_service_for_url

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getenv(env):
    """HACK use dev for running local unit/integration tests"""
    try:
        return os.environ[env]
    except:
        logging.warn(f"{env} missing, defaulting to {env}_DEV")
        return os.environ[env + '_DEV']

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
BASE_URL = "https://api.telegram.org/bot{}".format(TELEGRAM_TOKEN)

TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')
TELEGRAM_ALERT_GROUP = json.loads(os.environ['TELEGRAM_ALERT_GROUP'])

def handler(event, context):
    """Perform appropriate action for each endpoint invocation"""
    try:
        if event['path'] == "/hello":
            return {"statusCode": 200, "body": "hello, world!"}
        elif event['path'] == "/alert":
            return send_alert(event, context)
        elif event['path'] == "/webhookUpdate":
            return handle_webhook_update(event, context)
    except Exception as e:
        logging.error("Handling request", exc_info=True)
        return {"statusCode": 500}
    return {"statusCode": 404}

"""
Endpoint Handlers
"""

def send_alert(event, context):
    try:
        event_body = json.loads(event['body'])
        alerter = event_body['alerter']
    except Exception as e:
        logging.error("Processing alert request body", exc_info=True)
        return {"statusCode": 400}

    mentions = [f"@{u}" for u in TELEGRAM_ALERT_GROUP if u != alerter]
    response = (
        f":: TEAM ALERT ::\n"
        f"{alerter} Needs your help!\n"
        f"\n"
        f"{', '.join(mentions)}")
    return send_message(response, TELEGRAM_CHAT_ID)

def handle_webhook_update(event, context):
    event_body = json.loads(event['body'])

    try:
        msg_date = event_body['message']['date']
    except KeyError:
        logging.error("Parsing date from Telegram update")
        return {"statusCode": 400}

    # avoid spamming our APIs
    timeout = 30  # seconds
    age = datetime.datetime.now().timestamp() - msg_date
    logging.info(f"Telegram update age: {age}s")
    if age > timeout:
        logging.info(f"Ignoring old Telegram update")
        return {"statusCode": 200}

    try:
        text = event_body['message']['text']
    except KeyError:
        logging.error("Parsing text from Telegram update")
        return {"statusCode": 400}

    urls = urls_in_text(text)
    if urls:
        response = send_music_mirror_links(urls)
        if response['statusCode'] != 200:
            return response

    return {"statusCode": 200}

"""
Webhook Update Parsers
"""

def send_music_mirror_links(urls):
    similar_tracks = get_similar_tracks_from_urls(urls)
    if not similar_tracks:
        logging.info("No mirrors found for url")
        return {"statusCode": 200}

    logging.info(f"similar_tracks: {similar_tracks}") #TODO rm

    response = "Mirrors:\n"
    for idx, track_matches in enumerate(similar_tracks):
        if idx != 0:
            response += '\n\n'
        response += '\n'.join([f"* {svc_name}: {t.share_link()}" for svc_name, t in track_matches.items()])
    return send_message(response, TELEGRAM_CHAT_ID)

"""
Helpers
"""

def send_message(text, chat_id):
    try:
        data = {"text": text.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
    except Exception as e:
        logging.error("Encoding message", exc_info=True)
        return {"statusCode": 500}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(response.content)
        logging.error("Sending Telegram message", exc_info=True)
        return {"statusCode": 500}
    except requests.exceptions.RequestException as e:
        logging.error("Sending Telegram message", exc_info=True)
        return {"statusCode": 500}

    return {"statusCode": 200}

def urls_in_text(text):
    urls = [w for w in text.split(' ') if re.match('http[s]?://.*', w)]
    return urls

def get_similar_tracks_from_urls(urls):
    similar_tracks: List[Dict[str, StreamingServiceTrack]] = []
    logging.info(f"urls: {urls}") #TODO rm
    for url in urls:
        logging.info("URL detected")
        logging.info(url)
        svc = get_streaming_service_for_url(url)
        if svc:
            trackId = svc.get_trackId_from_url(url)
            logging.info(f"url: {url} ; trackId: {trackId}") #TODO rm
            try:
                with svc() as svc_client:
                    original_track = svc_client.get_track_from_trackId(trackId)
            except Exception as e:
                logging.error("Getting track from track id", exc_info=True)
                continue
            similar_tracks.append(get_similar_tracks_for_original_track(svc, original_track))
        else:
            logging.info("URL is not for a supported streaming service")
            continue
    return similar_tracks

def get_similar_tracks_for_original_track(track_svc, original_track):
    """Returns dict of urls from other streaming services for the same track"""
    similar_tracks: Dict[str, StreamingServiceTrack] = {}
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc is track_svc:
            continue
        with svc() as svc_client:
            try:
                track = svc_client.search_one_track(original_track.searchable_name)
                similar_tracks[svc.__name__] = track
            except:
                logging.error("Getting track from trackId", exc_info=True)
    return similar_tracks


if __name__ == '__main__':
    # Integration Tests
    text = """
    Hey! Check out these tracks!
    https://open.spotify.com/track/43ddJFnP8m3PzNJXiHuiyJ?si=T3ZApBErTF-M1esGJoRMmw
    https://youtu.be/_kvZpVMY89c
    https://open.spotify.com/track/1wnq9TwifJ9ipLUFsm8vKx?si=IUytRONLTYWxJz3g5L9y8g
    """
    event = { "body": json.dumps(
        {
            'update_id': 10000,
            'message': {
                'date': 1441645532,
                'chat': {
                    'last_name': 'Test Lastname',
                    'id': 1111111,
                    'first_name': 'Test',
                    'username': 'Test'
                },
                'message_id': 1365,
                'from': {
                    'last_name': 'Test Lastname',
                    'id': 1111111,
                    'first_name': 'Test',
                    'username': 'Test'
                },
                'text': text
            }
        }
    )}
    handle_webhook_update(event, None)
