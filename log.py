from logging import StreamHandler

import telegram


class TelegramLogHandler(StreamHandler):
    def __init__(self, telegram_base_url, telegram_chat_id):
        StreamHandler.__init__(self)
        self.telegram_base_url = telegram_base_url
        self.telegram_chat_id = telegram_chat_id

    def emit(self, record):
        msg = self.format(record)
        telegram.send_message()
