# Logging utility
import logging
import sys


class Logger:
    _loggers = {}

    def __init__(self, name: str):
        self.name = name
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging.INFO)
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            
            Logger._loggers[name] = logger
        
        self._logger = Logger._loggers[name]

    def info(self, message: str):
        self._logger.info(message)

    def error(self, message: str):
        self._logger.error(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def debug(self, message: str):
        self._logger.debug(message)
