import os
os.environ[
    "LOGURU_FORMAT"
] = "{time:DD.MM.YY HH:mm:s} [<lvl>{level:^10}</lvl>] <lvl>{message}</lvl>"
os.environ["LEVEL"] = "DEBUG"
from loguru import logger
