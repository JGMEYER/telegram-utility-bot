import logging
import os

from . import telegram


def setup_logger(logger_name):
    log = logging.getLogger(logger_name)

    # TODO this will break in prod / dev
    TELEGRAM_TOKEN_DEV = os.environ["TELEGRAM_TOKEN_DEV"]
    TELEGRAM_CHAT_ID_DEV = os.environ["TELEGRAM_CHAT_ID_DEV"]

    formatter = logging.Formatter("%(asctime)s : %(message)s")

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Create Telegram handler
    th = TelegramLogHandler(TELEGRAM_TOKEN_DEV, TELEGRAM_CHAT_ID_DEV)
    th.setLevel(logging.WARNING)
    th.setFormatter(formatter)
    log.addHandler(th)

    # TODO rm
    log.info(os.environ.get("TELEGRAM_TOKEN"))


class TelegramLogHandler(logging.StreamHandler):
    """StreamHandler for logging via Telegram messages"""

    def __init__(self, telegram_token, telegram_chat_id):
        logging.StreamHandler.__init__(self)
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def emit(self, record):
        """Send message to Telegram"""
        try:
            msg = self.format(record)
            telegram.send_message(
                self.telegram_token, self.telegram_chat_id, msg
            )
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
