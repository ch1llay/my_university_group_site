# -*- coding: utf-8 -*-

"""документация к коду"""

# TODO: Добавить список команд для бота в кнопку
# TODO: прочитать статьи про classmethod и staticmethod =>  => создать в бд сущность для хранения объектов класса User
# # TODO: метод для удаления сообщений по времени поточно ВАЖНО НО НЕ СРОЧНО!
# TODO: ВАЖНО СРОЧНО отправка сообщений обычным образом, все на обычных кнопках, нормальное добавление дз, получение дз(по предмету, по дате) получение расписания на день, неделю, добавить админов которые

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

import json
import random
import datetime as dt

import vk_api
from flask import Flask, request
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.bot.botdatabase.bd_commands import *
# from app.db.all_tools_db import *
from app.settings.config import *
from app.bot.botdatabase.bot_model import *


class Keyboards:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Меню", color=VkKeyboardColor.SECONDARY, payload={"payload": "menu"})
    keyboard.add_line()
    keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")
    # inline клавиатура для браузера
    menu = VkKeyboard(inline=True)
    menu.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"today"}')
    menu.add_callback_line()
    menu.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"tomorrow"}')
    menu.add_callback_line()
    menu.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"timetable"}')
    menu.add_callback_line()
    menu.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"prepody"}')
    menu.add_callback_line()
    menu.add_callback_button("Выйти", payload={"payload": "mainmenu"})
    # клавиатура для получения информации о преподавателях
    subjects_keyboard = VkKeyboard(inline=True)
    subjects_keyboard.add_callback_button("Английский", payload={"payload": "english"})
    subjects_keyboard.add_callback_button("ИТвПД", payload={"payload": "itvpd"})
    subjects_keyboard.add_callback_button("Математика", payload={"payload": "math"})
    subjects_keyboard.add_callback_button("МЛиТА", payload={"payload": "mlita"})
    subjects_keyboard.add_line()
    subjects_keyboard.add_callback_button("Правоведение", payload={"payload": "pravo"})
    subjects_keyboard.add_callback_button("Программирование", payload={"payload": "proga"})
    subjects_keyboard.add_callback_button("ТРИР", payload={"payload": "trir"})
    subjects_keyboard.add_callback_button("Физика", payload={"payload": "phisic"})
    subjects_keyboard.add_line()
    subjects_keyboard.add_callback_button("Назад", payload={"payload": "mainmenu"})

    def get_keyboard(self):
        return self.keyboard.get_keyboard()

    def get_menu(self):
        return self.menu.get_keyboard()

    def get_subjects_keyboard(self):
        return self.subjects_keyboard.get_keyboard()

token = cfg.get('vk', 'token')
vk = vk_api.VkApi(token=token).get_api()
class Bot:
    keyboard = Keyboards.get_keyboard()
    menu = Keyboards.get_menu()
    subjects_keyboard = Keyboards.get_keyboard()

    def get_week_number(self):
        today = datetime.today()
        weekday = today.weekday()
        wk = today.isocalendar()[1]
        if weekday < 6:
            number_week = 1 if wk % 2 else 2
        else:
            number_week = 2 if wk % 2 else 1
        return number_week

    @staticmethod
    def reply(self, **kwargs):
        general = dict(random_id=random.randint(0, 343439483948), keyboard=self.keyboard)
        general.update(kwargs)
        vk.messages.send(**general)

    def reply_with_event(peer_id, event_id, user_id, text):
        vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                event_data=json.dumps(
                                                    '{"type": "show_snackbar", "text": ' + text + ' }'))

    def delete_last_message(self, peer_id_):
        message_id = vk.messages.getHistory(count=1, peer_id=peer_id_)["items"][0]["id"]
        vk.messages.delete(message_ids=message_id, delete_for_all=True)
    @staticmethod
    def msg_processing(data):
        type_ = data["type"]
        message = data["object"]



app = Flask(__name__)
