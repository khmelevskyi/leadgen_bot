from telegram import Update
from telegram.ext import CallbackContext
import pandas as pd

from ...database import db_session
from ...database import Calls


def get_stats(update: Update, context: CallbackContext):
    

    db_session.get_stats()


# def query_to_dict(rset):
#     result = defaultdict(list)
#     for obj in rset:
#         instance = inspect(obj)
#         for key, x in instance.attrs.items():
#             result[key].append(x.value)
#     return result