import logging
import colorlog
import sys
import os

logger = logging.getLogger("")
level = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(level)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
)
sh.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S",
    )
)
logger.addHandler(sh)
