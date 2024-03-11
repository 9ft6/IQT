import json
from pathlib import Path
import pickle

from pydantic import BaseModel

from iqt.logger import logger


class DataNavigationState(BaseModel):
    page: int = 1
    per_page: int = 5
    sort_key: str = None
    filter: dict = {}


class Dataset:
    state: DataNavigationState
    items: dict
    dump_file: str | Path

    def __init__(self):
        logger.info("Loading strains dataset...")
        self.load()
        self.state = DataNavigationState()

    def __iter__(self):
        filtered = self._get_filtered()
        _sorted = list(sorted(filtered.keys()))
        page, per_page = self.state.page, self.state.per_page
        current_page = _sorted[page * per_page:page * per_page + per_page]
        result = [self.items[i] for i in current_page]
        return iter(result)

    def _get_filtered(self):
        filtered = self.items
        # TODO: Implement filter
        return filtered

    def count(self):
        return len(self._get_filtered())

    def set_page(self, page):
        self.state.page = page

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
