# -*- coding: utf-8 -*-

"""Документация к коду"""

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(os_split(__file__)[0])[0])[0])[0]]

import os

from datetime import date
from datetime import time
from datetime import datetime

from pony.orm import *

from app.db.db_base_func import AddArrtInDbClass

from app.settings.config import *

db = Database()

pony.options.CUT_TRACEBACK = False


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


class Phrase_(db.Entity):
    name = PrimaryKey(str)
    text = Optional(str)


class Rank(db.Entity):
    name = PrimaryKey(str)
    ids = Optional(Json)


def connect_with_db(db_path="", deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.8
    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        exit()

    if not isfile(db_path):
        db_l.connect(allow_auto_upgrade=True,
                     create_tables=True,
                     create_db=True,
                     provider="sqlite",
                     filename=db_path)
        print('create db')
    else:

        try:
            db_l.connect(allow_auto_upgrade=True,
                         provider=cfg.get("db", "type"),
                         filename=db_path)
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db_l.connect(allow_auto_upgrade=True,
                             create_tables=True,
                             # create_db=True,
                             provider="sqlite",
                             filename=db_path)
                print('получилось')
            except Exception as e:
                print("Начинаем миграцию")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                # controller_migration_version(db_path)
                print('\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....')
                print('\n=========================================')
                exit()


# connect_with_db(db_path="database.sqlite", db_l=db)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
# for name, ent in db.entities.items():
#     ent.__bases__ = (tuple(list(ent.__bases__) + [AddArrtInDbClass])
#                      if AddArrtInDbClass not in list(ent.__bases__)
#                      else tuple(list(ent.__bases__)))

# def ddd(cls, key1, key2='пр.'):
#     if type(cls) == type(Subject):
#         print('----', key1, key2)
#         cls.__getattribute__(key1, key2)
#
# setattr(Subject, "__getattribute__", classmethod(ddd))

# Subject.__getattribute__()
