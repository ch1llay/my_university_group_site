from itertools import chain

from app.bot.botdatabase.bot_model import *

PRAKTIKA = "пр."


def create_default_db():
    subjects = [{"name": "математика"},
                {"name": "математика", "type_subject": "лк."}
                ]
    [Subject(**i) for i in subjects]
    commit()


def add_subject(name, type_subject="пр."):
    Subject(name=name, type_subject=type_subject)
    commit()


def add_home_task(subject, text, task_date):
    Hometask(subject=subject, text=text, task_date=task_date)
    commit()


def get_default_db():
    return list(chain(Subject.select()[:]))


def get_home_task(subject, _id):
    subject.home_tasks.select(lambda i: i.id == _id)[:][0].text


def delete_home_task(subject, func=lambda i: True):
    [i.delete() for i in subject.home_tasks.select() if func(i)]


with db_session:
    add_home_task(Subject["математика", "пр."], "номер 1", "11.03.2021")
    # print(get_home_task(Subject["математика", "пр."], 1))
    print([i.text for i in Hometask.select(lambda i: i.task_date == date(2021, 3, 10))])
    print([i.text for i in Hometask.select(lambda i: i.task_date == date(2021, 3, 11))])
    delete_home_task(Subject["математика", "пр."], lambda i: i.task_date == date(2021, 3, 10)) # удалить все дз по математике
    print(list(map(lambda i: i.text, Hometask.select(lambda i: i.task_date == date(2021, 3, 10))[:]))) # получить всю домашку
    print(list(map(lambda i: i.text, Hometask.select(lambda i: i.task_date == date(2021, 3, 11))[:]))) # получить всю домашку