import os
import requests
import telegram
import feedparser

# Configurações
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RSS_URL = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"

bot = telegram.Bot(token=TOKEN)

def fetch_rss():
    feed = feedparser.parse(RSS_URL)
    noticias = []
    for entry in feed.entries[:5]:  # pega só as 5 últimas
        title = entry.title
        link = entry.link
        noticias.append((title, link))
    return noticias

def send_news():
    noticias = fetch_rss()
    if not noticias:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Nenhuma notícia encontrada no RSS.")
        return

    msg = "📰 Últimas notícias (RSS):\n\n"
    for title, link in noticias:
        msg += f"• [{title}]({link})\n"
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

if __name__ == "__main__":
    send_news()
