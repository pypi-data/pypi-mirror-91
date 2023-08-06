import logging
from .measures import Measures


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
sh.setFormatter(formatter)

logger.addHandler(sh)
