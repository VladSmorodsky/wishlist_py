from typing import TypedDict, NotRequired


class WishData(TypedDict):
    id: int
    name: NotRequired[str]
    description: NotRequired[str]
    url: NotRequired[str]
