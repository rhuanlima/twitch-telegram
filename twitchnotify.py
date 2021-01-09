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
streamers = ['bananaslamjamma', 'gunnardota2', 'monkeys_forever', 'xcaliburye', 'gorgc', 'purgegamers']

streamerstate = {}

for user_ids in streamers:
    streamerstate[user_ids] = 0


check_game = operations.check_game
bot = operations.send_telegram_photo
twitch = Twitch(ClientID, ClientSecret)

while True:

    twitch.authenticate_app([])
    for streamername in streamers:
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
            photo_url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streamername}-720x480.jpg"
            uptime = humanize.precisedelta(time_now - stream_start_time, minimum_unit='seconds')
            if check_game and streamerstate[streamername] == 0:
                bot(
                    f"{streamer} is now live playing {game_name}\nStream Title: {stream_title}\nViewers: {viewers}\nUptime: {uptime} ",
                    telegram_chat_id, telegram_token, photo_url)
                streamerstate[streamername] = 1
                pprint(f"{streamer} is now live {game_name} Stream Title: {stream_title}")
            else:
                pass
        else:
            streamerstate[streamername] = 0
    time.sleep(60)



