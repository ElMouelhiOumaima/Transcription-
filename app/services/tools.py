import os
from loguru import logger
def clean(path: str) -> bool:
    """
    remove a file after transcription
    :param path: path to file
    """
    try:
        os.remove(path)
        return True
    except FileNotFoundError:
        logger.error("File {} does not exist".format(path))
        return False