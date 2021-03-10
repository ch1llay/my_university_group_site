from app.bot.botdatabase.bd_commands import *


def executable(function):
    with db_session:
        return function()
