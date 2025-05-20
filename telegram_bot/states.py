from enum import Enum


class State(Enum):
    START = 0
    CREATE_WISH = 1
    WISH_NAME = 2
    WISH_DESCRIPTION = 3
    WISH_URL = 4
    END = 5
