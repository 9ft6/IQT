from typing import Literal


db_types = ["dict", "tinydb"]
DBType = Literal["dict", "tinydb"]


class Config:
    db_type: DBType = "tinydb"


cfg = Config()
