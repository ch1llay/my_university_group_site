from app.bot.botdatabase.bd_commands import *

# import vk_api
# TODO: добавить в базу данных пользователей(peer_ids) отправлять всем

today = datetime.today()
weekday = today.weekday()
number_week = 1 if today.isocalendar()[1] % 2 else 2

with db_session:
    timetable = [(i.time, i.subject, i.link) for i in Timetable.select() if i.number_week == number_week and i.weekday == weekday]
    timetable_s = f"{weekdays[weekday]}\n"
    for t, s, l in timetable:
        timetable_s += f"{t.hour}:{'00' if str(t.minute) == '0' else t.minute} {s.name} {s.type_subject} {l}\n"
    print(timetable_s)