#!/usr/bin/env python3
import os
import requests
import html
from datetime import datetime

# Variáveis de ambiente (configuradas nos Secrets do GitHub)
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def get_news():
    params = {
        "apiKey": NEWSAPI_KEY,
        "country": "br",
        "pageSize": 5
    }
    r = requests.get(NEWSAPI_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("articles", [])

def build_message(articles):
    if not articles:
        return "Nenhuma notícia encontrada."
    lines = []
    for art in articles[:3]:
        title = html.escape(art.get("title") or "")
        source = art.get("source", {}).get("name", "")
        url = art.get("url", "")
        lines.append(f"📰 <b>{title}</b>\n{source}\n{url}")
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"📢 Manchetes — {now}\n\n" + "\n\n".join(lines)

def send_message(text):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(TELEGRAM_URL, data=payload, timeout=10)
    r.raise_for_status()

if __name__ == "__main__":
    articles = get_news()
    msg = build_message(articles)
    send_message(msg)
    print("✅ Notícias enviadas com sucesso!")
