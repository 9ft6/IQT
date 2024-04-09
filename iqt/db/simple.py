import json
from pathlib import Path
import pickle

from iqt.logger import logger
from .base import DataBaseWrapper


class BaseDictDB(DataBaseWrapper):
    items: dict
    dump_file: str | Path = None

    def __init__(self):
        self.items = {}
        self.load()

    def query(self, state):
        filtered = self._get_filtered(self.items)
        _sorted = self._get_sorted(filtered, state)
        return self._get_current_page(_sorted, state)

    def _get_filtered(self, items):
        filtered = items
        # TODO: Implement filter
        return filtered

    def _get_sorted(self, filtered, state):
        key = state.sort_key or "id"
        return list(sorted(
            filtered.values(),
            reverse=state.ascending,
            **{"key": lambda s: str(getattr(s, key, ""))}
        ))

    def _get_current_page(self, _sorted, state):
        page, per_page = state.page, state.per_page
        return _sorted[(page - 1) * per_page:page * per_page]

    def remove(self, key):
        ...

    def remove_many(self, key):
        ...

    def insert(self, item):
        ...

    def insert_many(self, items):
        self.items.update({i.id: i for i in items})
        self.dump()

    def update_many(self, many):
        ...

    def update(self, key, value):
        ...

    def count(self, state=None):
        if not state:
            return len(self._get_filtered(self.items))

    def distinct(self, key):
        ...

    def show(self, _filter=None):
        for item in self.items.values():
            if not _filter or _filter(item):
                logger.info(item)

    def export(self):
        with open('export.json', 'w') as file:
            items = {i: s.dict() for i, s in self.items.items()}
            json.dump(items, file)

    def dump(self):
        if self.dump_file:
            try:
                with open(self.dump_file, 'wb') as file:
                    pickle.dump(self.items, file)
            except Exception as e:
                logger.error(f"Cannot write pickle {e}")

    def load(self):
        if self.dump_file:
            try:
                with open(self.dump_file, 'rb') as file:
                    self.items = pickle.load(file)
            except Exception as e:
                logger.error(f"Cannot read pickle {e}")


__all__ = ['BaseDictDB']
