from typing import Literal
from pathlib import Path

from pydantic import Field, BaseModel

from iqt.components.data_view.item import BaseDataItem
from iqt.components.data_view.dataset import Dataset


class Supply(BaseDataItem):
    _view_widgets: dict = {}
    _sort_fields: str = ["name", "slug", "category"]

    id: int = None
    rating: float = Field(None, description="Average rating")
    category: Literal["books", "other"] = Field(None, description="Category")
    name: str = Field(None, description="Strain name")
    image: str = Field(None, description="<preview>")
    slug: str | None = Field(None, description="Slug")
    subtitle: str = Field(None, description="<item_name>")
    discount: bool = Field(False, description="Discount")


class Supplies(Dataset):
    dump_file: Path = Path("supplies.pickle")
    item_model: BaseModel = Supply()
