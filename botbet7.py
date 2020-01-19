import requests
import vk_api
import urllib.request
import re
import docx
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession
from vk_api.longpoll import VkLongPoll, VkEventType

url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-%d1%80%d0%b0%d1%81%' \
      'd0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
all_text = []
another1 = []
days1 = []
domain = 'https://drive.google.com/'
s = requests.Session()
vk_session = vk_api.VkApi(token='5733815caa6fe4bc2564be1a322902f56a3b8e7ac2daaae36faf2ab26f632fe2501f89a070c55e15f5bb9')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
vk._auth_token()
vk.get_api()


def find():
    global all_links
    global all_text
    session = HTMLSession()
    html = session.get(url)
    bs = BeautifulSoup(html.text)
    link_list = bs.find('div', {'class': 'entry'})
    print(link_list)
    items = link_list.find_all('a')
    if len(all_links) > len(all_text) or len(all_text) > len(all_links):
        all_links = []
        all_text = []
    for item in items:
        link = item.get('href')
        text = item.text
        if link not in all_links:
            all_links.append(link)
        if text not in all_text:
            all_text.append(text)


def days():
    global days1
    days1 = []
    get_empty_keyboard()
    for opa in range(len(all_text)):
        if 'января (' in str(all_text[opa]):
            add_button(self, str(all_text[opa]), color='default')
            days1.append(all_text[opa])


def another():
    global another1
    another1 = []
    get_empty_keyboard()
    for opa in range(len(all_text)):
        if 'января (' not in str(all_text[opa]):
            add_button(self, str(all_text[opa]), color='default')
            another1.append(all_text[opa])


class VkKeyboard(object):
    __slots__ = ('one_time', 'lines', 'keyboard', 'inline')

    def __init__(self, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline
        self.lines = [[]]

        self.keyboard = {
            'one_time': self.one_time,
            'inline': self.inline,
            'buttons': self.lines
        }

        def get_keyboard(self):
            return sjson_dumps(self.keyboard)

    @classmethod
    def get_empty_keyboard(cls):
        keyboard = cls()
        keyboard.keyboard['buttons'] = []
        return keyboard.get_keyboard()

    def add_button(self, label, color=VkKeyboardColor.DEFAULT, payload=None):

        current_line = self.lines[-1]

        if len(current_line) >= 4:
            raise ValueError('Max 4 buttons on a line')

        color_value = color

        if isinstance(color, VkKeyboardColor):
            color_value = color_value.value

        if payload is not None and not isinstance(payload, six.string_types):
            payload = sjson_dumps(payload)

        button_type = VkKeyboardButton.TEXT.value

        current_line.append({
            'color': color_value,
            'action': {
                'type': button_type,
                'payload': payload,
                'label': label,
            }
        })


keyboardall = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Расписание"
            },
            "color": "primary"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Другое"
                },
                "color": "secondary"
            }
        ]
    ]
}

keyboardall = json.dumps(keyboardall, ensure_ascii=False).encode('utf-8')
keyboardall = str(keyboardall.decode('utf-8'))

longpoll = VkBotLongPoll(vk, club190878826)

while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.text.lower() == "Узнать":
                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "Выберите нужный пункт", "random_id": 0,
                                            "keyboard": keyboardall})
            if event.object.text.lower() == "Другое":
                another()
                vk.method("messages.send",
                          {"peer_id": event.object.peer_id, "message": "Выберите нужное из раздела Другое", "random_id": 0,
                           "keyboard": keyboard})
            if event.object.text.lower() == "Расписание":
                days()
                vk.method("messages.send",
                          {"peer_id": event.object.peer_id, "message": "Выберите нужное из раздела Расписание", "random_id": 0,
                           "keyboard": keyboard})
            if event.object.text.lower() in another1:
                curmess = another1.index(str(event.object.text.lower))
                curmessage = another1[curmess]
                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": curmessage, "random_id": 0
                                            })
            if event.object.text.lower() in days1:
                curmess = days1.index(str(event.object.text.lower))
                curmessage = days1[curmess]
                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": curmessage, "random_id": 0
                                            })
