import json
import pickle

from iqt.logger import logger
from .base import FileBasedDataBase


class BaseDictDB(FileBasedDataBase):
    items: dict

    def __init__(self):
        self.items = {}
        self.load()

    def _get_filtered(self, state):
        return self.items

    def _get_sorted(self, filtered, state):
        key = state.sort_key or "id"
        return list(sorted(
            filtered.values(),
            reverse=state.ascending,
            key=lambda s: str(getattr(s, key, "")),
        ))

    def insert_many(self, items):
        self.items.update({i.id: i for i in items})
        self.dump()

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
