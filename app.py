import os
import datetime
import humanize
from twitchAPI.twitch import Twitch
import telegram
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv('./.env')

class Live:
    def __init__(self, nome):
        self.nome = nome
        self.ClientID = os.environ["clientid"]
        self.ClientSecret = os.environ["clientsecret"]
        self.telegram_token = os.environ["telegramtoken"]
        self.telegram_chat_id = os.environ["telegramchatid"]
        self.yt_canal = os.environ["ytcanal"]

    def _check_live(self):
        twitch = Twitch(self.ClientID, self.ClientSecret)
        twitch.authenticate_app([])
        data_streams = twitch.get_streams(user_login=[self.nome])
        return data_streams

    def check_live(self):
        data_streams = self._check_live()
        print("check")
        if data_streams["data"]:
            self.live_id = data_streams["data"][0]["id"]
            self.live_photo_url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{self.nome}-720x480.jpg"
            self.live_photo_msg = data_streams["data"][0]["title"]
            self.live_photo_chat_id = self.telegram_chat_id
            self.live_photo_token = self.telegram_token
            stream_start_time = datetime.datetime.strptime(
                data_streams["data"][0]["started_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
            time_now = datetime.datetime.utcnow()
            self.uptime = humanize.precisedelta(
                time_now - stream_start_time, minimum_unit="seconds"
            )
            self.alert_live_on()
            self.save_live()

    def _get_connection(self):
        conn = sqlite3.connect("lives.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS lives (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                live_id varchar(255) NOT NULL,
                dt_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
        return (conn, cursor)

    def _save_live(self, conn, cursor, nome, live_id):
        cursor.execute(
            f"""
        INSERT INTO lives (nome, live_id) VALUES ('{nome}', '{live_id}')
        """
        )
        conn.commit()

    def _get_last_live(self, conn, cursor):
        cursor.execute(
            """
        SELECT live_id FROM lives WHERE dt_created = (SELECT MAX(dt_created) FROM lives)
        """
        )
        last_live = cursor.fetchone()
        return last_live[0] if last_live else None

    def _close_connection(self, conn):
        conn.close()

    def _send_telegram_photo(self, msg, chat_id, token, photo_url):
        bot = telegram.Bot(token=token)
        bot.send_photo(chat_id=chat_id, caption=msg, photo=photo_url)

    def _send_telegram_message(self, msg, chat_id, token):
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id, text=msg)

    def alert_live_on(self):
        conn, cursor = self._get_connection()
        last_live = self._get_last_live(conn, cursor)
        if last_live != self.live_id:
            self._send_telegram_photo(
                f"{self.nome} Esta online!!! \nLive: {self.live_photo_msg}\nTempo de Live: {self.uptime}\nLink: https://www.twitch.tv/{self.nome} ",
                self.live_photo_chat_id,
                self.live_photo_token,
                self.live_photo_url,
            )
        self._close_connection(conn)

    def save_live(self):
        conn, cursor = self._get_connection()
        last_live = self._get_last_live(conn, cursor)
        if last_live != self.live_id:
            self._save_live(conn, cursor, self.nome, self.live_id)
        self._close_connection(conn)

    def check_youtube(self):
        url = f"https://www.youtube.com/channel/{self.yt_canal}/live"
        ret = requests.get(url)
        soup = BeautifulSoup(ret.text, "html.parser")
        if "Ao vivo".lower() in ret.text.lower():
            print(f"Streaming: {url}")


live = Live(os.getenv("nome"))
scheduler = BlockingScheduler()
scheduler.add_job(live.check_live, "interval", seconds=10)
scheduler.start()
