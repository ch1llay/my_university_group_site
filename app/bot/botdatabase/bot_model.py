# -*- coding: utf-8 -*-

"""Документация к коду"""

from datetime import date
from datetime import time
from datetime import datetime

from pony.orm import *

from app.db.db_base_func import AddArrtInDbClass

db = Database()


class Timetable(db.Entity):
    id = PrimaryKey(int, auto=True)
    subject = Optional('Subject')
    number_week = Optional(int)
    weekday = Optional(int)
    time = Optional(time)
    link = Optional(str)  # ссылка на конференцию или номер аудитории


class Subject(db.Entity):
    name = Required(str)
    type_subject = Required(str, default="пр.")
    time_tables = Set(Timetable)
    home_tasks = Set('Hometask')
    teachers = Set('Teacher')
    PrimaryKey(name, type_subject)


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


for name, ent in db.entities.items():
    ent.__bases__ = (tuple(list(ent.__bases__) + [AddArrtInDbClass])
                     if AddArrtInDbClass not in list(ent.__bases__)
                     else tuple(list(ent.__bases__)))

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
