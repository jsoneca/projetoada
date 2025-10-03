import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import telegram
import os

BASE_URL = "https://sbtnews.sbt.com.br/noticias"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TOKEN)

def fetch_news():
    resp = requests.get(BASE_URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    noticias = []
    for a in soup.select("h2 a, h3 a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and (href.startswith("/noticia") or href.startswith("/noticias/")):
            link = urljoin("https://sbtnews.sbt.com.br", href)
            noticias.append((title, link))

    seen = set()
    clean = []
    for t, l in noticias:
        if l not in seen:
            seen.add(l)
            clean.append((t, l))
    return clean

def send_news():
    noticias = fetch_news()[:5]
    if not noticias:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Nenhuma notícia encontrada.")
        return
    msg = "📰 Últimas do SBT News:\n\n"
    for title, link in noticias:
        msg += f"• [{title}]({link})\n"
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

if __name__ == "__main__":
    send_news()
