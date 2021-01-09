import os
import time
import datetime
import humanize
from pprint import pprint

from twitchAPI.twitch import Twitch

import operations

ClientID = os.environ['clientid']
ClientSecret = os.environ['clientsecret']
telegram_token = os.environ['telegramtoken']
telegram_chat_id = os.environ['telegramchatid']

state = 0

streamername = 'xcaliburye'

check_game = operations.check_game
bot = operations.send_telegram_photo
twitch = Twitch(ClientID, ClientSecret)

while True:

    twitch.authenticate_app([])
    #data = twitch.get_streams(user_login=['bananaslamjamma'])
    data = twitch.get_streams(user_login=[streamername])
    if data['data']:
        streamer = data['data'][0]['user_name']
        game_id = data['data'][0]['game_id']
        game_name = data['data'][0]['game_name']
        stream_title = data['data'][0]['title']
        viewers = data['data'][0]['viewer_count']
        check_game(game_id, game_name)
        stream_start_time = datetime.datetime.strptime(data['data'][0]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
        time_now = datetime.datetime.utcnow()
        uptime = humanize.precisedelta(time_now - stream_start_time, minimum_unit='seconds')
        if check_game and state == 0:
            bot("{} is now live {} \nStream Title: {}\nViewers: {}\nUptime: {} ".format(streamer, game_name, stream_title, viewers, uptime),
                telegram_chat_id, telegram_token, streamername)
            state = 1
            pprint("{} is now live {} Stream Title: {}".format(streamer, game_name, stream_title))
        else:
            pass
    else:
        state = 0
    time.sleep(60)



