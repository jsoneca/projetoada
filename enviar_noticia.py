import os
import telegram
import feedparser

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Suporte para múltiplos grupos/usuários
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")

RSS_URL = "https://rss.app/feeds/pKg4lz64NExm8UkK.xml"

def fetch_rss():
    feed = feedparser.parse(RSS_URL)
    noticias = []
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        desc = entry.get("summary", "")
        # pegar só 3 linhas (máx. 200 caracteres)
        short_desc = " ".join(desc.split()[:40]) + "..."
        # pegar imagem (se existir)
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
        caption = f"📰 *{noticia['title']}*\n\n{noticia['desc']}\n\n👉 [Ler mais]({noticia['link']})"

        for chat in CHAT_IDS:
            if noticia["image"]:
                # Envia com imagem
                bot.send_photo(chat_id=chat, photo=noticia["image"], caption=caption, parse_mode="Markdown")
            else:
                # Sem imagem
                bot.send_message(chat_id=chat, text=caption, parse_mode="Markdown")

if __name__ == "__main__":
    send_news()
