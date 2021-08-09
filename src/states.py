""" bot states for conversation handler """
from enum import Enum


class States(Enum):
    """ states keys """

    PASSWORD_CHECK = 0

    ADMIN_MENU = 1

    ADMIN_CALL_CHOSEN = 2

    HAS_CALL_BEEN = 3

    CALL_NO_DESCRIPTION = 4