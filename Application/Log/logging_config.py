# logger_config.py
import logging

def setup_logger():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename='app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s\n',
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='w'
        )
    return logging

def reset_logger():
    # Get the root logger
    logger = logging.getLogger()
    
    # Remove all handlers associated with the root logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Reconfigure the logger as per your needs
    logging.basicConfig(level=logging.INFO)  # Set log level and other configuration


