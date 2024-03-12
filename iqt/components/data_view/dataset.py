import json
from pathlib import Path
import pickle

from pydantic import BaseModel

from iqt.logger import logger


class DataNavigationState(BaseModel):
    page: int = 1
    per_page: int = 50
    sort_key: str = None
    filter: dict = {}
    ascending: bool = True


class Dataset:
    state: DataNavigationState
    items: dict
    dump_file: str | Path
    item_model: BaseModel

    def __init__(self, update_callback):
        self.update_callback = update_callback
        logger.info("Loading strains dataset...")
        self.load()
        self.state = DataNavigationState()
        self.per_page = self.state.per_page

    def __iter__(self):
        filtered = self._get_filtered(self.items)
        _sorted = self._get_sorted(filtered)
        return iter(self._get_current_page(_sorted))

    def _get_filtered(self, items):
        filtered = items
        # TODO: Implement filter
        return filtered

    def _get_sorted(self, filtered):
        kwargs = {"key": lambda s: getattr(s, self.state.sort_key or "id", "")}
        return list(sorted(filtered.values(), reverse=self.state.ascending, **kwargs))

    def _get_current_page(self, _sorted):
        page, per_page = self.state.page, self.state.per_page
        return _sorted[(page - 1) * per_page:page * per_page]

    def get_sort_fields(self):
        # TODO: implement dynamic fields generation
        return self.item_model.sort_fields

    def count(self):
        return len(self._get_filtered(self.items))

    def set_ascending(self, ascending: bool):
        if self.state.ascending != ascending:
            self.state.ascending = ascending

    def set_sort_key(self, key):
        if self.state.sort_key != key:
            self.state.sort_key = key
            self.update_callback()

    def set_page(self, page):
        if self.state.page != page:
            self.state.page = page
            self.update_callback()

    def show(self, _filter=None):
        for item in self.items.values():
            if not _filter or _filter(item):
                logger.info(item)

    def export(self):
        with open('export.json', 'w') as file:
            items = {i: s.dict() for i, s in self.items.items()}
            json.dump(items, file)

    def dump(self):
        with open(self.dump_file, 'wb') as file:
            pickle.dump(self.items, file)

    def load(self):
        try:
            with open(self.dump_file, 'rb') as file:
                self.items = pickle.load(file)
        except Exception as e:
            logger.error(f"Cannot read strains.pickle {e}")
