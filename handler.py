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
    if event['path'] == "/hello":
        return {"statusCode": 200, "body": "hello, world!"}
    elif event['path'] == "/alert":
        return telegram_alert(event, context)
    elif event['path'] == "/musicConverter":
        return telegram_music_convert(event, context)
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

def telegram_music_convert(event, context):
    return {"statusCode": 200}

def urls_in_message(msg):
    urls = [w for w in msg.split(' ') if re.match('http[s]?://.*', w)]
    return urls

def get_similar_tracks_from_msg(msg):
    """Parses message for urls and returns matches for similar streaming tracks"""
    urls = urls_in_message(msg)
    if not urls:
        return
    similar_tracks: List[Dict[str, StreamingServiceTrack]] = []
    for url in urls:
        logging.info("URL detected")
        logging.info(url)
        svc = get_streaming_service_for_url(url)
        if svc:
            trackId = svc.get_trackId_from_url(url)
            with svc() as svc_client:
                original_track = svc_client.get_track_from_trackId(trackId)
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
    import pprint
    pprint.pprint(get_similar_tracks_from_msg('https://open.spotify.com/track/43ddJFnP8m3PzNJXiHuiyJ?si=T3ZApBErTF-M1esGJoRMmw'))
    pprint.pprint(get_similar_tracks_from_msg('https://youtu.be/_kvZpVMY89c'))
    pprint.pprint('https://open.spotify.com/track/1wnq9TwifJ9ipLUFsm8vKx?si=IUytRONLTYWxJz3g5L9y8g')
