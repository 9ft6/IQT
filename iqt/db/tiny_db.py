from tempfile import NamedTemporaryFile

from pydantic import BaseModel
from tinydb import TinyDB as TinyDataBase, Query

from iqt.logger import logger
from .base import FileBasedDataBase


class TinyDB(FileBasedDataBase):
    db: TinyDataBase
    item_model: BaseModel

    def __init__(self):
        if file := self.dump_file or NamedTemporaryFile().name:
            self.db = TinyDataBase(file)
        else:
            logger.error(f"TinyDB dump file not specified")

    def query(self, state):
        return [self.item_model.parse_obj(i) for i in super().query(state)]

    def _get_filtered(self, state):
        return self.db.all()

    def _get_sorted(self, filtered, state):
        return list(sorted(
            filtered,
            reverse=state.ascending,
            key=lambda s: s.get(state.sort_key or "id"),
        ))

    def insert_many(self, items):
        self.db.insert_multiple(x.model_dump() for x in items)


__all__ = ["TinyDB"]
