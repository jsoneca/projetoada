import os
import feedparser
import html
from bs4 import BeautifulSoup
from telegram import Bot

# === Configurações ===
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = [c.strip() for c in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if c.strip()]

RSS_FEED = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"

bot = Bot(token=TOKEN)

def clean_html(raw_html, max_length=200):
    """Remove tags HTML e limita o tamanho do texto"""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(" ", strip=True)
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."
    return text

def get_news():
    feed = feedparser.parse(RSS_FEED)
    noticias = []

    for entry in feed.entries[:3]:
        title = html.escape(entry.title)
        link = entry.link

        desc_raw = entry.summary if hasattr(entry, "summary") else ""
        desc = clean_html(desc_raw, max_length=200)

        image = None
        if "media_content" in entry and len(entry.media_content) > 0:
            image = entry.media_content[0].get("url")

        noticias.append({
            "title": title,
            "link": link,
            "desc": desc,
            "image": image
        })

    return noticias

def send_news():
    noticias = get_news()

    for noticia in noticias:
        caption = f"<b>{noticia['title']}</b>\n\n{noticia['desc']}\n\n👉 <a href='{noticia['link']}'>Ler mais</a>"

        for chat in CHAT_IDS:
            try:
                if noticia["image"]:
                    bot.send_photo(chat_id=chat, photo=noticia["image"], caption=caption, parse_mode="HTML")
                else:
                    bot.send_message(chat_id=chat, text=caption, parse_mode="HTML")
            except Exception as e:
                print(f"Erro ao enviar para {chat}: {e}")

if __name__ == "__main__":
    send_news()
