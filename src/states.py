""" bot states for conversation handler """
from enum import Enum


class States(Enum):
    """ states keys """

    PASSWORD_CHECK = 0

    ADMIN_MENU = 1