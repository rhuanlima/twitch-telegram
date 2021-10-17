import requests
from bs4 import BeautifulSoup


canais = [
    "UCjE-fonhL546FyL2VJ51JNw",
    "UCKESyc4OGHHV-flWwr3VBWA",
    "AndreSionek",
    "Coreanofps",
    "UCuiLR4p6wQ3xLEm15pEn1Xw",
]

for canal in canais:
    url = f"https://www.youtube.com/channel/{canal}/live"
    ret = requests.get(url)
    soup = BeautifulSoup(ret.text, "html.parser")
    if "Ao vivo".lower() in ret.text.lower():
        print(f"Streaming: {url}")
