import requests
import telebot
import urllib3
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-' \
      '%d1%80%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
domain = 'https://drive.google.com/'


def find_urls():
    global all_links
    try:
        res = requests.get(url, timeout=30)
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, 'error')
    soup = BeautifulSoup(res.text, 'lxml')
    for link in soup.find_all('a', href=True):
        if link['href'][0] == '#':
            pass
        elif link['href'][0] == '/':
            pass
        else:
            all_links.add(link['href'])


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        find_urls()
        bot.send_message(chat_id, str(all_links))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
