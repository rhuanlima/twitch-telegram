import telegram
from string import Formatter
from datetime import timedelta

def check_game(game_id, game_name):
    if game_id == '29595' or game_name == "Dota 2":
        return True
    else:
        pass


def send_telegram_photo(msg, chat_id, token, streamername):
    """
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""

    bot = telegram.Bot(token=token)
    bot.send_photo(chat_id=chat_id, caption=msg,
                   photo="https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-720x480.jpg"
                   .format(streamername))


def send_telegram_message(msg, chat_id, token):
    """
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
