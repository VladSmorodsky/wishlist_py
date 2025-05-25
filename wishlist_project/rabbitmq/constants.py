from enum import Enum

WISH_EXCHANGE_NAME = 'wish_management'
TELEGRAM_REQUEST_QUEUE = 'telegram_request'
WISH_QUEUE_NAME = 'wish'


class BindEvent(Enum):
    CREATE_WISH = f'{TELEGRAM_REQUEST_QUEUE}.create_wish_request'
    GET_WISHES = f'{WISH_QUEUE_NAME}.get_all'
    GET_WISHES_REQUEST = f'{TELEGRAM_REQUEST_QUEUE}.get_wishlist_request'
    WISH_EVENT_ERROR = f'{WISH_QUEUE_NAME}.error'
    WISH_EVENT_SUCCESS = f'{WISH_QUEUE_NAME}.success'
