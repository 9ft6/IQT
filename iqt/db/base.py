from abc import abstractmethod
from pathlib import Path


class DataBaseWrapper:
    @abstractmethod
    def query(self, state):
        ...

    @abstractmethod
    def remove(self, key):
        ...

    @abstractmethod
    def remove_many(self, key):
        ...

    @abstractmethod
    def insert(self, item):
        ...

    @abstractmethod
    def insert_many(self, items):
        ...

    @abstractmethod
    def update_many(self, many):
        ...

    @abstractmethod
    def update(self, key, value):
        ...

    @abstractmethod
    def count(self, key):
        ...

    @abstractmethod
    def distinct(self, key):
        ...


class FileBasedDataBase(DataBaseWrapper):
    dump_file: str | Path = None

    def count(self, state=None):
        if not state:
            return len(self._get_filtered(state))

    def query(self, state):
        filtered = self._get_filtered(state)
        _sorted = self._get_sorted(filtered, state)
        return self._get_current_page(_sorted, state)

    def _get_filtered(self, state) -> iter:
        ...

    def _get_sorted(self, filtered, state):
        ...

    def _get_current_page(self, _sorted, state):
        page, per_page = state.page, state.per_page
        return _sorted[(page - 1) * per_page:page * per_page]


__all__ = ['DataBaseWrapper', 'FileBasedDataBase']
