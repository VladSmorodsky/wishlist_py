import json
from abc import ABC, abstractmethod

from accounts.models import User
from logger import get_logger
from rabbitmq.constants import BindEvent
from rabbitmq.publisher import publish
from rabbitmq.schemas import WishData
from wishlist_app.models import Wish

logger = get_logger(__name__)

class WishEventHandler(ABC):
    """
    Abstract handler class
    """

    @abstractmethod
    def handle(self, wish_data: dict = None):
        pass


class TelegramWishCreateHandler(WishEventHandler):
    def handle(self, wish_data: WishData = None):
        if wish_data is None:
            return None
        user = User.objects.filter(telegram_id=wish_data['id']).first()
        if not user:
            logger.error("Please provide a telegram_id into your settings")
            publish(json.dumps({'error': "Please provide a telegram_id into your settings"}).encode("utf-8"), BindEvent.WISH_EVENT_ERROR)
            return None
        Wish.objects.create(user=user, name=wish_data['name'], description=wish_data['description'],
                            url=wish_data['url'])


class WishListHandler(WishEventHandler):
    def handle(self, wish_data: dict = None):
        user = User.objects.filter(telegram_id=wish_data['id']).first()
        if not user:
            logger.error("Please provide a telegram_id into your settings")
            publish(json.dumps({'error': "Please provide a telegram_id into your settings"}).encode("utf-8"), BindEvent.WISH_EVENT_ERROR)
            return None
        wish_list_queryset = Wish.objects.filter(user=user).values("name", "description", "url")
        wish_list = list(wish_list_queryset)
        publish(message=json.dumps({'wish_list': wish_list}).encode("utf-8"), routing_key=BindEvent.GET_WISHES)


class WishEventRegister:
    handlers: dict[str, WishEventHandler] = {}

    def add_handler(self, bind_event: BindEvent, handler: WishEventHandler):
        self.handlers[bind_event.value] = handler

    def remove_handler(self, bind_event: BindEvent) -> None:
        self.handlers.pop(bind_event.value, None)


def get_wish_event_register():
    wish_event_register = WishEventRegister()
    wish_event_register.add_handler(BindEvent.CREATE_WISH, TelegramWishCreateHandler())
    wish_event_register.add_handler(BindEvent.GET_WISHES_REQUEST, WishListHandler())
    return wish_event_register
