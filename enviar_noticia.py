import os
import telegram
import feedparser
import html

# Configurações do bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# IDs separados por vírgula no secret TELEGRAM_CHAT_IDS
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")

# RSS do SBT News (via rss.app)
RSS_URL = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"


def fetch_rss():
    feed = feedparser.parse(RSS_URL)
    noticias = []
    for entry in feed.entries[:5]:  # pega as 5 últimas
        title = entry.title
        link = entry.link
        desc = entry.get("summary", "")

        # limitar tamanho do resumo (~3 linhas)
        short_desc = " ".join(desc.split()[:40]) + "..."

        # tentar pegar imagem
        image = None
        if "media_content" in entry and entry.media_content:
            image = entry.media_content[0].get("url")
        elif "media_thumbnail" in entry and entry.media_thumbnail:
            image = entry.media_thumbnail[0].get("url")

        noticias.append({
            "title": title,
            "link": link,
            "desc": short_desc,
            "image": image
        })
    return noticias


def send_news():
    noticias = fetch_rss()
    if not noticias:
        for chat in CHAT_IDS:
            bot.send_message(chat_id=chat, text="⚠️ Nenhuma notícia encontrada no RSS.")
        return

    for noticia in noticias:
        # escapar caracteres especiais para HTML
        title = html.escape(noticia['title'])
        desc = html.escape(noticia['desc'])
        link = noticia['link']

        caption = f"<b>{title}</b>\n\n{desc}\n\n👉 <a href='{link}'>Ler mais</a>"

        for chat in CHAT_IDS:
            if noticia["image"]:
                bot.send_photo(
                    chat_id=chat,
                    photo=noticia["image"],
                    caption=caption,
                    parse_mode="HTML"
                )
            else:
                bot.send_message(
                    chat_id=chat,
                    text=caption,
                    parse_mode="HTML"
                )


if __name__ == "__main__":
    send_news()
