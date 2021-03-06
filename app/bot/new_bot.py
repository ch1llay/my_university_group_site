# -*- coding: utf-8 -*-

"""документация к коду"""

# TODO: Добавить список команд для бота в кнопку

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

import json
import random

import vk_api
from flask import Flask, request
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.bot.data import *
# from app.db.all_tools_db import *
from app.settings.config import *
from app.bot.botdatabase.bot_model import *