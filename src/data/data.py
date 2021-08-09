# -*- coding: utf-8 -*-
""" additional data """
import json
import os
import re

import pytz

directory_path = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
new_path = os.path.join(directory_path, "texts.json")

with open(new_path, "r", encoding="utf-8") as fp:
    text = json.load(fp)


TIMER_RANGE = [6, 10]

kiev_tz = os.getenv("TIME_ZONE", "Europe/Kiev")
TIME_ZONE = pytz.timezone(kiev_tz)