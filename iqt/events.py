from typing import Any

from pydantic import BaseModel


class BusEvent(BaseModel):
    target: str
    sender: str = None
    type: str
    message: Any


class BasePopupEvent(BusEvent):
    target: str = "popup"

    def __init__(self, message: str):
        super().__init__(message=message)


class OpenPopupEvent(BasePopupEvent):
    type: str = "open_popup"
    

class ClosePopupEvent(BasePopupEvent):
    type: str = "close_popup"


class SetPopupEvent(BasePopupEvent):
    type: str = "set_popup"
