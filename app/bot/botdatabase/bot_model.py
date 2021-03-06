# -*- coding: utf-8 -*-

"""Документация к коду"""

from datetime import date
from datetime import time
from datetime import datetime

from pony.orm import *

db = Database()


class Timetable(db.Entity):
    id = PrimaryKey(int, auto=True)
    subject = Optional('Subject')
    week_number = Optional(int)
    weekday = Optional(int)
    time = Optional(time)


class Subject(db.Entity):
    name = PrimaryKey(str)
    home_task = Optional(str)
    time_tables = Set(Timetable)
    home_tasks = Set('Hometask')
    teachers = Set('Teacher')


class Hometask(db.Entity):
    id = PrimaryKey(int, auto=True)
    subject = Optional(Subject)
    text = Optional(str)
    task_on_photo = Optional(Json)
    task_date = Optional(date)
    task_time = Optional(time)
    messages_ids = Optional(Json)  # адишники пересланных сообщений с дз например фото


class Teacher(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    subjects = Set(Subject)
    email = Optional(str)
    phone_number = Optional(str)
    vk_url = Optional(str)


db.generate_mapping()
