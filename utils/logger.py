import logging
from src.main import LOG_LEVEL , BASE_DIR
import os 

def logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    log_dir =os.path.join(BASE_DIR, "LOG_FILES")
    os.makedirs(log_dir , exist_ok=True)
    
    log_file_path = os.path.join(log_dir , "LOG_FILES.txt")
    
    
    if not logger.hasHandlers():
    # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)
        # File Handler 
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(LOG_LEVEL)
    # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
    # add ch to logger
        logger.addHandler(ch)
        logger.daddHandler(fh)
    return logger