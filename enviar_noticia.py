import os
import requests
import telegram
import feedparser

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Vários grupos/usuários
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")
RSS_URL = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"

def fetch_rss():
    feed = feedparser.parse(RSS_URL)
    noticias = []
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        noticias.append((title, link))
    return noticias

def send_news():
    noticias = fetch_rss()
    if not noticias:
        for chat in CHAT_IDS:
            bot.send_message(chat_id=chat, text="⚠️ Nenhuma notícia encontrada.")
        return

    msg = "📰 Últimas notícias de hoje ☕️\n\n"
    for title, link in noticias:
        msg += f"• [{title}]({link})\n"

    for chat in CHAT_IDS:
        bot.send_message(chat_id=chat, text=msg, parse_mode="Markdown")

if __name__ == "__main__":
    send_news()
