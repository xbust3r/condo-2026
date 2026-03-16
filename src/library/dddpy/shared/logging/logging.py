import logging
from typing import Optional, Any


class Logger:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name
        self.inside_method: Optional[str] = None
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)

    def add_inside_method(self, method_name: Optional[str]):
        self.inside_method = method_name
        return self

    def clear_inside_method(self):
        self.inside_method = None
        return self

    def _build_message(self, data: Any) -> str:
        method = self.inside_method or "-"
        return f"{self.logger_name} - {method} - {data}"

    def log(self, level: str, data: Any):
        log_function = getattr(self.logger, level)
        return log_function(self._build_message(data))

    def info(self, data: Any):
        return self.log("info", data)

    def debug(self, data: Any):
        return self.log("debug", data)

    def warning(self, data: Any):
        return self.log("warning", data)

    def error(self, data: Any):
        return self.log("error", data)

    def critical(self, data: Any):
        return self.log("critical", data)
