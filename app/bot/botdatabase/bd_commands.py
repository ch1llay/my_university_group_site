if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(os_split(__file__)[0])[0])[0])[0]]

from itertools import chain

from app.bot.botdatabase.bot_model import *

import datetime as dt

PRAKTIKA = "пр."
LEKCIA = "лк."


@db_session
def create_default_db():
    subjects = [{"name": "математика"},
                {"name": "математика", "type_subject": "лк."},

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

                {"name": "английский 1"},
                {"name": "английский 2"},

                {"name": "кураторский час", "type_subject": "-"},
                {"name": "физ-ра", "type_subject": "-"},
                ]
    [Subject(**i) for i in subjects]
    commit()
    teachers = [
        dict(name="Купряшина Лилия Александовна", subjects=Subject.select(lambda i: i.name == "математика")[:]),
        dict(name="Костина Наталья Владимировна",
             subjects=[Subject["физика", PRAKTIKA]]),
        dict(name="Суровицкая Галина Владимировна",
             subjects=[Subject["физика", LEKCIA]]),
        dict(name="Гурьянов Лев Вячеславович", subjects=Subject.select(lambda i: i.name == "программирование")[:]),
        dict(name="Такташкин Денис Витальевич", subjects=Subject.select(lambda i: i.name == "трир")[:]),
        dict(name="Голобокова Елена Михайловна",
             subjects=[Subject["итвпд", PRAKTIKA]]),
        dict(name="Данкова Наталья Владамировна",
             subjects=[Subject["английский 1", PRAKTIKA]]),
        dict(name="Юрасова Ольга Владимировна",
             subjects=[Subject["английский 2", PRAKTIKA]])
    ]
    [Teacher(**i) for i in teachers]
    commit()
    timetable = [
        {"number_week": 1, "subject": Subject["физика", PRAKTIKA], "time": time(11, 40), "link": "8-507",
         "weekday": 0},
        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "time": time(13, 45), "link": "8-216",
         "weekday": 0},

        {"number_week": 1, "subject": Subject["математика", PRAKTIKA], "time": time(9, 50), "link": "7б-205",
         "weekday": 1},
        {"number_week": 1, "subject": Subject["физ-ра", "-"], "time": time(11, 40), "link": "",
         "weekday": 1},
        {"number_week": 1, "subject": Subject["итвпд", PRAKTIKA], "time": time(13, 45), "link": "7а-405а",
         "weekday": 1},

        {"number_week": 1, "subject": Subject["трир", LEKCIA], "time": time(9, 50), "link": "7а-425", "weekday": 2},
        {"number_week": 1, "subject": Subject["программирование", LEKCIA], "time": time(11, 40), "link": "7а-418",
         "weekday": 2},
        {"number_week": 1, "subject": Subject["программирование", PRAKTIKA], "time": time(13, 45), "link": "7а-307",
         "weekday": 2},

        {"number_week": 1, "subject": Subject["физика", LEKCIA], "time": time(8, 0),
         "link": r"https://us04web.zoom.us/j/3881678889?pwd=KzlRejJ0dnB6SCszOVVzSkhOUm9UUT09#success",
         "weekday": 3},
        {"number_week": 1, "subject": Subject["математика", LEKCIA], "time": time(9, 50),
         "link": r"https://us04web.zoom.us/j/75974098629?pwd=MUxSMDZ4bnBaeElaQ1llMmJzekVTdz09#success",
         "weekday": 3},
        {"number_week": 1, "subject": Subject["млита", PRAKTIKA], "time": time(11, 40),
         "link": r"https://us04web.zoom.us/j/74153390010?pwd=RXdZRUVRMWJUd29GczYwSDhJNC9YZz09",
         "weekday": 3},

        {"number_week": 1, "subject": Subject["трир", PRAKTIKA], "time": time(8, 8), "link": "7а-108",
         "weekday": 4},
        {"number_week": 1, "subject": Subject["английский 1", PRAKTIKA], "time": time(9, 50), "link": "8-807",
         "weekday": 4},
        {"number_week": 1, "subject": Subject["английский 2", PRAKTIKA], "time": time(9, 50), "link": "8-807б",
         "weekday": 4},
        {"number_week": 1, "subject": Subject["физ-ра", "-"], "time": time(11, 40), "link": "",
         "weekday": 4},

        {"number_week": 1, "subject": Subject["правоведение", LEKCIA], "time": time(8, 0),
         "link": r"https://us04web.zoom.us/j/5981307260?pwd=VDBhWnFzUUtLVlBNWEUzS2Z3em5Ydz09",
         "weekday": 5},
        {"number_week": 1, "subject": Subject["млита", PRAKTIKA], "time": time(9, 50),
         "link": "https://us04web.zoom.us/j/74153390010?pwd=RXdZRUVRMWJUd29GczYwSDhJNC9YZz09",
         "weekday": 5},

        {"number_week": 2, "subject": Subject["кураторский час", "-"], "time": time(9, 50), "link": "7а-307",
         "weekday": 0},
        {"number_week": 2, "subject": Subject["физика", PRAKTIKA], "time": time(11, 40), "link": "",
         "weekday": 0},

        {"number_week": 2, "subject": Subject["математика", PRAKTIKA], "time": time(9, 50), "link": "7б-205",
         "weekday": 1},
        {"number_week": 2, "subject": Subject["физ-ра", "-"], "time": time(11, 40), "link": "",
         "weekday": 1},
        {"number_week": 2, "subject": Subject["итвпд", PRAKTIKA], "time": time(13, 45), "link": "7а-405а",
         "weekday": 1},

        {"number_week": 2, "subject": Subject["программирование", LEKCIA], "time": time(11, 40), "link": "7а-418",
         "weekday": 2},
        {"number_week": 2, "subject": Subject["программирование", PRAKTIKA], "time": time(13, 45), "link": "7а-307",
         "weekday": 2},
        {"number_week": 2, "subject": Subject["правоведение", PRAKTIKA], "time": time(15, 35), "link": "7а-425",
         "weekday": 2},

        {"number_week": 2, "subject": Subject["физика", LEKCIA], "time": time(8, 0),
         "link": r"https://us04web.zoom.us/j/3881678889?pwd=KzlRejJ0dnB6SCszOVVzSkhOUm9UUT09#success", "weekday": 3},
        {"number_week": 2, "subject": Subject["математика", LEKCIA], "time": time(9, 50),
         "link": r"https://us04web.zoom.us/j/75974098629?pwd=MUxSMDZ4bnBaeElaQ1llMmJzekVTdz09#success",
         "weekday": 3},

        {"number_week": 2, "subject": Subject["трир", PRAKTIKA], "time": time(8, 0), "link": "7а-108", "weekday": 4},
        {"number_week": 2, "subject": Subject["английский 1", PRAKTIKA], "time": time(9, 50), "link": "8-807",
         "weekday": 4},
        {"number_week": 2, "subject": Subject["английский 2", PRAKTIKA], "time": time(9, 50), "link": "8-807б",
         "weekday": 4},
        {"number_week": 2, "subject": Subject["физ-ра", "-"], "time": time(11, 40), "link": "",
         "weekday": 4}
    ]
    [Timetable(**i) for i in timetable]
    commit()

    phrases = [
        dict(name="start",
             text="Привет! У меня ты сможешь узнать расписание, домашнее задание, и что-нибудь еще, если это что-то в меня добавят)"),
        dict(name="timetable",
             text="""1)8:00-9:35\n2)9:50-11:25\n3)11:40-13:15\n4)13:45-15:20\n5)15:35-17:10"""),
    ]

    [Phrase_(**i) for i in phrases]
    commit()

    admins = [
        dict(name="write_homework",
             ids="159526068,334465281,285983191,100774328,259258321,222458536,307097759,430256596,239105355,166287013,211900416,368974771,209567456")
    ]


weekdays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


@db_session
def add_subject(name, type_subject="пр."):
    Subject(name=name, type_subject=type_subject)
    commit()


@Subject.only_func
@db_session
def add_home_task(subject, text, date_year_month_day_):
    Hometask(subject=subject, text=text, task_date=date(*date_year_month_day_))
    commit()


@db_session
def get_default_db():
    return list(chain(Subject.select()[:]))


@Subject.only_func
@db_session
def delete_home_task_from_date(subject, date_year_month_day_):
    [i.delete() for i in subject.home_tasks.select() if lambda i: i.task_date == date(*date_year_month_day_)]


@db_session
def delete_home_task_date(date_year_month_day_):
    map(lambda i: i.delete(),
        Hometask.select(lambda i: i.task_date == date(*date_year_month_day_))[:])  # получить всю домашку


@db_session
def get_home_task(date_year_month_day_=None) -> list:
    task = []
    if not date_year_month_day_:
        task = list(map(lambda i: i.text, Hometask.select(lambda i: True)[:]))
    else:
        task = [(i.text, i.task_date) for i in Hometask.select() if i.task_date == date(*date_year_month_day_)]
    return task


@Subject.only_func
@db_session
def get_home_task(subject, date_year_month_day_=None) -> list:
    task = []
    if not date_year_month_day_:
        task = [i.text for i in subject.home_tasks.select()]
    else:
        task = [i.text for i in subject.home_tasks.select() if i.task_date == date(*date_year_month_day_)]
    return task


@Subject.only_func
@db_session
def get_teachers(subject):
    return [i.name for i in subject.teachers]


# number_week = 1 if day.isocalendar()[1] % 2 else 2
@db_session
def get_timetable_day(day):
    msg = ""
    weekday = day.weekday() if day.weekday() < 6 else 0
    wk = day.isocalendar()[1]
    if day.weekday() < 6:
        number_week = 1 if wk % 2 else 2
    else:
        msg = "Я тебя понял, расписание на понедельник следующей недели"
        number_week = 2 if wk % 2 else 1
    timetable = [(i.time, i.subject, i.link) for i in Timetable.select() if
                 i.number_week == number_week and i.weekday == weekday]
    timetable_s = f"{msg}\n{weekdays[weekday]}\n"
    print(weekday, number_week)
    print(str(timetable))
    for t, s, l in timetable:
        timetable_s += f"{t.hour}:{'00' if str(t.minute) == '0' else t.minute} {s.name} {s.type_subject} {l}\n"
        print(timetable_s)
    return timetable_s


@db_session
def get_timetable_week():
    msg = ""
    today = datetime.today()
    weekday = today.weekday()
    wk = today.isocalendar()[1]
    print(weekday)
    if weekday < 6:
        number_week = 1 if wk % 2 else 2
        if weekday == 5 and today.time().hour > 10:
            msg = "Я тебя понял, даю расписанию на следующую неделю"
            number_week = 2 if wk % 2 else 1

    else:
        msg = "Я тебя понял, даю расписанию на следующую неделю"
        number_week = 2 if wk % 2 else 1
    timetable = [(i.weekday, i.time, i.subject, i.link) for i in Timetable.select() if
                 i.number_week == number_week]
    timetable_s = f"{msg}\nнеделя {number_week}\n"
    for wd, t, s, l in timetable:
        timetable_s += f"{weekdays[wd]}\n{t.hour}:{'00' if str(t.minute) == '0' else t.minute} {s.name} {s.type_subject} {l}\n"
    return timetable_s


@db_session
def get_phrase(name):
    return Phrase_[name].text


def executable(function):
    with db_session:
        return function()


if __name__ == "__main__":
    create_default_db()
    print(get_phrase("start"))
# get_timetable_day(datetime.today().date())
# with db_session:
# create_default_db()
# print(Subject.__class_getitem__())
# print(get_timetable_day((datetime.today()+dt.timedelta(days=1)).date()))
# print(Subject["математика", PRAKTIKA])
# # create_default_db()
#     # sbjt = "английский 2"
#     # subject_type = PRAKTIKA
#     # subject = Subject[sbjt, subject_type]
#     # subject.add_home_task("подготовить топик", (2021, 3, 11))
#     # # subject.delete_home_task_from_date((2021, 3, 11))
#     # print(subject.get_home_task((2021, 3, 11)))
#     print([i.subject for i in Timetable.select() if i.weekday == 0 and i.number_week == 1])
