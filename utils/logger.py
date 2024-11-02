import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Set up a logger with the specified name, log file, and level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create file handler which logs messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

# Example usage:
# game_logger = setup_logger('game_logger', 'logs/game.log')
# game_logger.info('Game started.')
# game_logger.error('An error occurred.')
