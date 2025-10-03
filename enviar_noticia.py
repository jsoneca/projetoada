import os
import feedparser
import html
from telegram import Bot

# === Configurações ===
TOKEN = os.getenv("TELEGRAM_TOKEN")  # seu token do Bot
CHAT_IDS = [c.strip() for c in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if c.strip()]  # lista de grupos

# RSS do SBT News (via rss.app)
RSS_FEED = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"

bot = Bot(token=TOKEN)

def get_news():
    """Busca as últimas notícias do RSS"""
    feed = feedparser.parse(RSS_FEED)
    noticias = []

    for entry in feed.entries[:3]:  # pega só as 3 últimas
        title = html.escape(entry.title)
        link = entry.link
        desc = html.escape(entry.summary) if hasattr(entry, "summary") else ""

        # tenta pegar imagem se existir
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
    """Envia notícias formatadas para os grupos"""
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
