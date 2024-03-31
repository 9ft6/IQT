from typing import Literal
from pathlib import Path

from pydantic import Field, BaseModel

from iqt.components.data_view.dataset.ds import Dataset
from iqt.components.data_view.dataset.item import BaseDataItem

Category = Literal["books", "buds", "other"] | None


class Accessory(BaseDataItem):
    _sort_fields: list = ["name", "rating", "category"]
    id: int = Field(None, description="ID")
    color: str | None = Field(None, description="Color")
    name: str | None = Field(None, description="Name")


class Supply(BaseDataItem):
    _sort_fields: list = ["name", "rating", "category"]

    id: int = Field(None, description="ID")
    accessories: list[Accessory] = Field([], description="Accessories")
    rating: float = Field(None, description="Rating")
    category: Category = Field(None, description="Category")
    name: str = Field(None, description="Name")
    image: str = Field(None, description="<preview>")
    slug: str | None = Field(None, description="Slug")
    subtitle: str = Field(None, description="<item_name>")
    discount: bool = Field(False, description="Discount")


class Supplies(Dataset):
    dump_file: Path = Path("supplies.pickle")
    item_model: BaseModel = Supply()
