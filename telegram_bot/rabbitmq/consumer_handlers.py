import os
from abc import ABC, abstractmethod

from telegram import Bot

from rabbitmq.constants import BindEvent

bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))


class WishEventHandler(ABC):
    """
    Abstract handler class
    """

    @abstractmethod
    async def handle(self, wish_data: dict = None):
        pass


class WishListHandler(WishEventHandler):
    async def handle(self, wish_data: dict = None):
        message = ''
        for wish in wish_data['wish_list']:
            message = message + f"- {wish['name']}\n{wish['description']}\n{wish['url']}\n\n"
        await bot.send_message(365155424, message)


class WishEventRegister:
    handlers: dict[str, WishEventHandler] = {}

    def add_handler(self, bind_event: BindEvent, handler: WishEventHandler):
        self.handlers[bind_event.value] = handler

    def remove_handler(self, bind_event: BindEvent) -> None:
        self.handlers.pop(bind_event.value, None)


def get_wish_event_register():
    wish_event_register = WishEventRegister()
    wish_event_register.add_handler(BindEvent.GET_WISHES, WishListHandler())
    return wish_event_register
