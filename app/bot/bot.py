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


class Keyboards:
    @staticmethod
    def get_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Меню", color=VkKeyboardColor.SECONDARY, payload={"payload": "menu"})
        keyboard.add_line()
        keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")
        return keyboard.get_keyboard()

    @staticmethod
    def get_menu():
        # inline клавиатура для браузера
        menu = VkKeyboard(inline=True)
        menu.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"today"}')
        menu.add_line()
        menu.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"tomorrow"}')
        menu.add_line()
        menu.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"timetable"}')
        menu.add_line()
        menu.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE,
                                 payload='{"payload":"teachers"}')
        menu.add_line()
        menu.add_callback_button("Выйти", payload={"payload": "mainmenu"})

        return menu.get_keyboard()

    @staticmethod
    def get_subjects_keyboard():
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
        subjects_keyboard.add_callback_button("Назад", payload={"payload": "menu"})
        return subjects_keyboard.get_keyboard()


token = cfg.get('vk', 'token')
vk = vk_api.VkApi(token=token).get_api()


class Bot:
    keyboard = Keyboards.get_keyboard()
    menu = Keyboards.get_menu()
    subjects_keyboard = Keyboards.get_keyboard()

    @staticmethod
    def reply(**kwargs):
        general = dict(random_id=random.randint(0, 343439483948), keyboard=Keyboards.get_keyboard())
        general.update(kwargs)
        vk.messages.send(**general)

    @staticmethod
    def reply_with_event(peer_id, event_id, user_id, text):
        vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                           event_data=json.dumps(
                                               '{"type": "show_snackbar", "text": ' + text + ' }'))

    # def delete_last_message(peer_id_):
    #     message_id = vk.messages.getHistory(count=1, peer_id=peer_id_)["items"][0]["id"]
    #     vk.messages.delete(message_ids=message_id, delete_for_all=True
    @staticmethod
    @db_session
    def msg_processing(data):
        type_ = data["type"]
        # print(type_)
        if type_ == 'confirmation':
            return cfg.get('vk', 'confirmation')
        elif type_ in ("message_new", "message_event"):
            if type_ == "message_new":
                message = data["object"]["message"]
                # print(message)
                from_id = message["from_id"]
                peer_id = message["peer_id"]
                payload = message.get("payload")
                send_method = Bot.reply
            elif "message_event":
                peer_id = data["object"]["peer_id"]
                user_id = data["object"]["user_id"]
                payload = data["object"]["payload"]
                event_id = data["object"]["event_id"]
                # vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                #                                    event_data=json.dumps(
                #                                        '{"type": "show_snackbar", "text": "всплыающее"}'))
                # send_method = Bot.reply_with_event
                print("event_id", event_id, type(event_id))
                # Bot.reply_with_event(peer_id=peer_id, event_id=event_id, user_id=user_id, text="Всплывающее")
            print("payload:", payload)
            if payload:
                payload = payload["payload"]
                command = payload
            else:
                text = message["text"]  # TODO: отлавливать обращение
                if "] " in text:
                    text = text.split("] ")[1]
                command = text
            base_msg = dict(peer_id=peer_id, keyboard=Bot.keyboard)
            commands = [
                {["start"]: dict(msg_text_fnctn=lambda: get_phrase("start"))},
                {["today"]: dict(msg_text_fnctn=lambda: get_timetable_day(datetime.today().date()))},
                {["tommorow"]: dict(
                    msg_text_fnctn=lambda: get_timetable_day((datetime.today() + dt.timedelta(days=1)).date()))},
                {["week"]: dict(msg_text_fnctn=lambda: get_timetable_week())},
                {["timetable"]: dict(msg_text_fnctn=lambda: get_phrase("timetable"))},
                {["teachers"]: dict(msg_text_fnctn=lambda: "Выберете предмет", keyboard=Bot.subjects_keyboard)},
                {["menu", "меню"]: dict(msg_text_fnctn=lambda: "Вы вернулись в главное меню", keyboard=Bot.menu)}
            ]
            for cmnds in commands:
                for c, d, in cmnds.items():
                    if command.lower() in c:
                        message = d["msg_text_fnctn"]()
                        if len(message) < 15:
                            message += "ничего)"
                        print(message)
                        d.pop("msg_text_fnctn")
                        base_msg.update({"message": message})
                        base_msg.update(d)
                    else:
                        print(command.lower(), c)

            Bot.reply(**base_msg)
        return "ok"


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def bot():
    if request.data:
        data = json.loads(request.data)
        r = Bot.msg_processing(data)
        if r != "ok":
            return r
    return "ok"

if __name__ == "__main__":
    app.run(

    )
