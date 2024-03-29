from typing import Literal
from pathlib import Path

from pydantic import Field, BaseModel

from iqt.components.data_view.item import BaseDataItem
from iqt.components.data_view.dataset import Dataset


class Accessory(BaseDataItem):
    _view_widgets: dict = {}

    id: int = Field(None, description="ID")
    color: str | None = Field(None, description="Color")


class Supply(BaseDataItem):
    _view_widgets: dict = {}
    _sort_fields: str = ["name", "rating", "category"]

    id: int = Field(None, description="ID")
    rating: float = Field(None, description="Rating")
    category: Literal["books", "buds", "other"] = Field(None, description="Category")
    name: str = Field(None, description="Name")
    image: str = Field(None, description="<preview>")
    slug: str | None = Field(None, description="Slug")
    subtitle: str = Field(None, description="<item_name>")
    discount: bool = Field(False, description="Discount")
    accessory: Accessory = Field(None, description="Accessoies")


class Supplies(Dataset):
    dump_file: Path = Path("supplies.pickle")
    item_model: BaseModel = Supply()
