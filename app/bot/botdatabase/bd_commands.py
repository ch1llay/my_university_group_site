from itertools import chain

from app.bot.botdatabase.bot_model import *

PRAKTIKA = "пр."
LEKCIA = "лк."


def create_default_db():
    teachers =
    subjects = [{"name": "математика"},
                {"name": "математика", "type_subject": "лк.", "teachers":Teacher["айдишник"]},

                {"name": "программирование"},
                {"name": "программирование", "type_subject": "лк."},

                {"name": "физика"},
                {"name": "физика", "type_subject": "лк."},

                {"name": "правоведение"},
                {"name": "правоведение", "type_subject": "лк."},

                {"name": "трир"},
                {"name": "трир", "type_subject": "лк."},

                {"name": "итвпд"},
                {"name": "млита"},
                {"name": "млита", "type_subject": "лк."},

                {"name": "физра", "type_subject": "пр. лк."},
                ]
    timetable = [
        {"number_week": 1, "subject": Subject["физика", PRAKTIKA], "weekday": "понедельник"},
        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "понедельник"},

        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "вторник"},
        {"number_week": 1, "subject": Subject["физ-ра", "пр. лк."], "weekday": "вторник"},
        {"number_week": 1, "subject": Subject["итвпд", PRAKTIKA], "weekday": "вторник"},

        {"number_week": 1, "subject": Subject["трир", LEKCIA], "weekday": "среда"},
        {"number_week": 1, "subject": Subject["программирование", LEKCIA], "weekday": "среда"},
        {"number_week": 1, "subject": Subject["программирование", PRAKTIKA], "weekday": "среда"},

        {"number_week": 1, "subject": Subject["физика", LEKCIA], "weekday": "четверг"},
        {"number_week": 1, "subject": Subject["математика", LEKCIA], "weekday": "четверг"},
        {"number_week": 1, "subject": Subject["млита", PRAKTIKA], "weekday": "четверг"},

        {"number_week": 1, "subject": Subject["трир", PRAKTIKA], "weekday": "пятница"},
        {"number_week": 1, "subject": Subject["английский(", PRAKTIKA], "weekday": "пятница"},
        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "пятница"},
        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "пятница"},

        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "суббота"},
        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "weekday": "суббота"}
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


def executable(function):
    with db_session:
        function()
