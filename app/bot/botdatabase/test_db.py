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


def add_home_task(subject, text, date_year_month_day_):
    Hometask(subject=subject, text=text, task_date=date(*date_year_month_day_))
    commit()


def get_default_db():
    return list(chain(Subject.select()[:]))


def delete_home_task_from_date_for_subject(subject, date_year_month_day_):
    [i.delete() for i in subject.home_tasks.select() if lambda i: i.task_date == date(*date_year_month_day_)]


def delete_home_task_date(date_year_month_day_):
    map(lambda i: i.delete(),
        Hometask.select(lambda i: i.task_date == date(*date_year_month_day_))[:])  # получить всю домашку


def get_home_task(date_year_month_day_=None) -> list:
    task = []
    if not date_year_month_day_:
        task = list(map(lambda i: i.text, Hometask.select(lambda i: True)[:]))
    else:
        task = list(map(lambda i: i.text, Hometask.select(lambda i: i.task_date == date(*date_year_month_day_))[:]))
    return task


def get_home_task_for_subject(subject, date_year_month_day_=None) -> list:
    task = []
    if not date_year_month_day_:
        task = [i.text for i in subject.home_tasks.select()]
    else:
        task = [i.text for i in subject.home_tasks.select() if i.task_date == date(*date_year_month_day_)]
    return task


with db_session:
    add_home_task(Subject["математика", "пр."], "номер 5", (2021, 3, 12))
    print(get_home_task_for_subject(Subject["математика", "пр."], (2021, 3, 12)))
