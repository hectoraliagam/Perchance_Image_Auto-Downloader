import logging

def setup_logger(name: str = __name__) -> logging.Logger:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    logger.addHandler(console_handler)
    logger.propagate = False
    
    return logger
