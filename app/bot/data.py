raspisanie_par = """1)8:00-9:35
2)9:50-11:25
3)11:40-13:15
4)13:45-15:20
5)15:35-17:10"""

Phrase(name="timetable",
           text="Привет! У меня ты сможешь узнать расписание, домашнее задание, и что-нибудь еще, если это что-то в меня добавят)")
Phrase(name="timetable",
           text="""1)8:00-9:35
2)9:50-11:25
3)11:40-13:15
4)13:45-15:20
5)15:35-17:10""")

with open("app/bot/raspisanie_first_week.txt", encoding="utf-8") as f:
    raspisanie_first_week = f.read()
with open("app/bot/raspisanie_second_week.txt", encoding="utf-8") as f:
    raspisanie_second_week = f.read()
