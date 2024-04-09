from pydantic import BaseModel

from iqt.db import BaseDictDB


class DataNavigationState(BaseModel):
    page: int = 1
    per_page: int = 25
    sort_key: str = None
    filter: dict = {}
    ascending: bool = True


class Dataset(BaseDictDB):
    state: DataNavigationState
    item_model: BaseModel

    def __init__(self, update_callback=None):
        super().__init__()
        self.update_callback = update_callback
        self.state = DataNavigationState()
        self.per_page = self.state.per_page

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

    def put_raws(self, raws: dict):
        self.insert_many(self.item_model.parse_obj(r) for r in raws.values())

