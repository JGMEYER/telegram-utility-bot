import logging

from . import telegram
from .env import getenv


def setup_logger(logger_name):
    log = logging.getLogger(logger_name)

    formatter = logging.Formatter("%(asctime)s : %(message)s")

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Create Telegram handler
    telegram_log_token = getenv("TELEGRAM_LOG_TOKEN")
    telegram_log_chat_id = getenv("TELEGRAM_LOG_CHAT_ID")
    th = TelegramLogHandler(telegram_log_token, telegram_log_chat_id)
    th.setLevel(logging.WARNING)
    th.setFormatter(formatter)
    log.addHandler(th)


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
