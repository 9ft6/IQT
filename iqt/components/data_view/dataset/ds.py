from typing import Any
from pydantic import BaseModel

from iqt.config import cfg
from iqt.db import BaseDictDB, TinyDB
from iqt.logger import logger


class DataNavigationState(BaseModel):
    page: int = 1
    per_page: int = 25
    sort_key: str = None
    filter: list = []
    ascending: bool = True
    dataset: Any = None
    model: BaseModel = None

    def __init__(self, dataset, **kwargs):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.model = dataset.item_model

    def add_filter(self, key, rule):
        if key in self.model.filter_fields:
            self.filter.append((key, rule))

    def remove_filter(self, key=None):
        for i, k, _ in enumerate(self.filter):
            if k == key:
                self.filter.remove(i)


class Dataset:
    state: DataNavigationState
    item_model: BaseModel

    def __init__(self, update_callback=None):
        super().__init__()
        self.update_callback = update_callback
        self.state = DataNavigationState(self)
        self.per_page = self.state.per_page
        self.add_filter = self.state.add_filter
        self.remove_filter = self.state.remove_filter

    def __iter__(self):
        return iter(self.query(self.state))

    def get_sort_fields(self):
        # TODO: implement dynamic fields generation
        return self.item_model.sort_fields

    def pages_count(self):
        return len(self.pages())

    def pages(self):
        pages = self.count() // self.per_page
        tail = self.count() % self.per_page
        return [x + 1 for x in range(0, pages + bool(tail))]

    def set_ascending(self, ascending: bool):
        if self.state.ascending != ascending:
            self.state.ascending = ascending
            if self.update_callback:
                self.update_callback()

    def set_sort_key(self, key):
        if self.state.sort_key != key:
            self.state.sort_key = key
            self.update_callback()

    def set_page(self, page):
        if self.state.page != page:
            self.state.page = page
            self.update_callback()

    def put_raws(self, raws: list):
        self.insert_many([self.item_model.parse_obj(r) for r in raws])


def get_dataset(update_callback=None):
    match cfg.db_type:
        case 'dict':
            db = BaseDictDB
        case 'tinydb':
            db = TinyDB
        case _:
            db = None
            logger.error(f'unknown db type: {cfg.db_type}')

    return type(
        "Dataset",
        (Dataset, db),
        {"update_callback": update_callback}
    )
