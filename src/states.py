""" bot states for conversation handler """
from enum import Enum


class States(Enum):
    """ states keys """

    PASSWORD_CHECK = 0

    ADMIN_MENU = 1

    ADMIN_CALL_CHOSEN = 2

    HAS_CALL_BEEN = 3

    CALL_NO_DESCRIPTION = 4

    CALL_PLAN_DATE = 5

    CALL_PLAN_TIME = 6

    CALL_PLAN_LINK = 7

    MAIN_MENU = 8

    NAME_AND_SURNAME = 9

    REPORT = 10

    CONNECTS = 11

    CHANGE_CONNECTS_WANT = 12

    CHANGE_CONNECTS = 13

    STATS_MENU = 14

    MAKE_ADMIN = 15

    MAKE_ADMIN_SAVE = 16