# -*- coding: utf-8 -*-

"""документация к коду"""

# TODO: Добавить список команд для бота в кнопку

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
    # обычная клавиатура, работающая с официального мобильного клиента, позволяет вывести inline клавиатуру для браузерной версии
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Альтернативное меню", color=VkKeyboardColor.SECONDARY, payload={"payload": "alternative_menu"})
    keyboard.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"today"}')
    keyboard.add_line()
    keyboard.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"tomorrow"}')
    keyboard.add_line()
    keyboard.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"timetable"}')
    keyboard.add_line()
    keyboard.add_callback_button("Defend", color=VkKeyboardColor.NEGATIVE,
                                 payload={"payload": "defend"})
    keyboard.add_line()
    keyboard.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"prepody"}')
    keyboard.add_line()
    keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")
    # inline клавиатура для браузера
    alternative_keyboard = VkKeyboard(inline=True)
    alternative_keyboard.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"today"}')
    alternative_keyboard.add_callback_line()
    alternative_keyboard.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"tomorrow"}')
    alternative_keyboard.add_callback_line()
    alternative_keyboard.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"timetable"}')
    alternative_keyboard.add_callback_line()
    alternative_keyboard.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE,
                                             payload='{"payload":"prepody"}')
    alternative_keyboard.add_callback_line()
    alternative_keyboard.add_callback_button("Выйти", payload={"payload": "mainmenu"})
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
    subjects_keyboard.

    def get_keyboard(self):
        return self.keyboard.get_keyboard()

    def get_alternative_keyboard(self):
        return self.alternative_keyboard.get_keyboard()

    def get_subjects_keyboard(self):
        return self.subjects_keyboard.get_keyboard()


class Bot:
    def __init__(self):
        token = cfg.get('vk', 'token')
        self.vk = vk_api.VkApi(token=token).get_api()
        self.keyboard = Keyboards.get_keyboard()
        self.alternative_keyboard = Keyboards.get_alternative_keyboard()
        self.subjects_keyboard = Keyboards.get_keyboard()

    def get_week_number(self):
        today = datetime.today()
        weekday = today.weekday()
        wk = today.isocalendar()[1]
        if weekday < 6:
            number_week = 1 if wk % 2 else 2
        else:
            number_week = 2 if wk % 2 else 1
        return number_week

    def reply(self, **kwargs):
        general = dict(random_id=random.randint(0, 343439483948), keyboard=self.keyboard)
        general.update(kwargs)
        self.vk.messages.send(**general)

    def reply_with_event(self, peer_id, event_id, user_id, text):
        self.vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                event_data=json.dumps(
                                                    '{"type": "show_snackbar", "text": ' + text + ' }'))

    def delete_last_message(self, peer_id_):
        message_id = self.vk.messages.getHistory(count=1, peer_id=peer_id_)["items"][0]["id"]
        self.vk.messages.delete(message_ids=message_id, delete_for_all=True)

    def smart_msg_creator(self, text, send_method, type_param="show_snackbar"):
        if type(send_method) == type(self.vk.messages.sendMessageEventAnswer):
            data = dict(event_data=json.dumps({
                "type": type_param,
                "text": text,
            }))
        else:
            data = dict(message=text)
        return data

    def processing_msg(self, command: str, data: dict, send_method=100):
        if send_method == 100:
            send_method = self.vk.messages.sendMessageEventAnswer
        if type(send_method) == type(self.vk.messages.sendMessageEventAnswer):
            user_id = data["object"]["user_id"]
            peer_id = data["object"]["peer_id"]
            print('callback-------------', data["object"])
            payload = command = data["object"]["payload"].get('payload', '-')
            # print(payload)
            basic_data_msg = dict(
                peer_id=peer_id,
                event_id=data["object"]["event_id"],
                user_id=user_id,
            )
        else:
            message = data['object']["message"]
            from_id = message["from_id"]
            peer_id = message['peer_id']
            basic_data_msg = dict(peer_id=peer_id, keyboard=self.keyboard)
            payload = message.get('payload')
            if payload:
                # Парсинг payload
                if type(payload) == str:
                    print("payload - str")
                    payload = [i.split(':') for i in payload.lstrip('{').rstrip('}').split(',')]
                    payload = {key.strip().strip('"').strip("'"): val.strip().strip('"').strip("'")
                               for [key, val] in payload}
                    print(payload)
                    payload = payload.get('payload')
                    print(payload)
                elif type(payload) == dict:
                    print("payload - dict")
                    payload = payload.get('payload')
            print(payload)
            command = payload or command.split()[0].lstrip('/')
            print(command)

            # main work
            if command == "start":
                ans = get_phrase("start")
                send_method = self.reply
                basic_data_msg = dict(peer_id=peer_id, message=ans)
            elif command == "week":
                send_method = self.reply
                basic_data_msg = dict(peer_id=peer_id, message=get_timetable_week(self.get_week_number()))
            elif command == "today":
                basic_data_msg.update(self.smart_msg_creator(get_timetable_day(datetime.today().date()), send_method))
            elif command == "tomorrow":
                basic_data_msg.update(
                    self.smart_msg_creator(get_timetable_day((datetime.today() + dt.timedelta(days=1)).date()),
                                           send_method))
            elif command == "timetable":
                basic_data_msg.update(self.smart_msg_creator(get_phrase("timetable"), send_method))


app = Flask(__name__)
