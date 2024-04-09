import abc


class DataBaseWrapper:
    @abc.abstractmethod
    def query(self, state):
        ...

    @abc.abstractmethod
    def remove(self, key):
        ...

    @abc.abstractmethod
    def remove_many(self, key):
        ...

    @abc.abstractmethod
    def insert(self, item):
        ...

    @abc.abstractmethod
    def insert_many(self, items):
        ...

    @abc.abstractmethod
    def update_many(self, many):
        ...

    @abc.abstractmethod
    def update(self, key, value):
        ...

    @abc.abstractmethod
    def count(self, key):
        ...

    @abc.abstractmethod
    def distinct(self, key):
        ...


__all__ = ['DataBaseWrapper']
