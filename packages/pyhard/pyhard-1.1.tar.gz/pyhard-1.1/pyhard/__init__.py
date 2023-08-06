import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .measures import Measures


log_file = Path(__file__).parents[2] / "graphene.log"

# clear the file every startup
with open(log_file, 'w'):
    pass

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# sh = logging.StreamHandler()
# sh.setLevel(logging.INFO)

# fh = logging.FileHandler(file)
fh = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)
fh.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
# sh.setFormatter(formatter)
fh.setFormatter(formatter)

# logger.addHandler(sh)
logger.addHandler(fh)
