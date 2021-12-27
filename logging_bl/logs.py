import logging


class BLLogger(logging.Logger):

    def __init__(self):
        super(BLLogger, self).__init__(__name__)
        self.setLevel(logging.DEBUG)

    def add_file_handler(self, log_file: str, log_format: str, level: int, mode: str = "a"):
        """Add a handler that logs to a file"""

        handler = logging.FileHandler(filename=log_file, mode=mode)
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        handler.setLevel(level)

        self.addHandler(handler)

    def add_console_handler(self, log_format: str, level: int):
        """Add a handler that logs to the console"""

        handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        handler.setLevel(level)

        self.addHandler(handler)


if __name__ == '__main__':
    my_new_logger = BLLogger()
    my_new_logger.add_file_handler(log_file="../../Output/Log files/test-log-file.log",
                                   level=logging.ERROR,
                                   log_format="%(name)s %(asctime)s %(levelname)s %(message)s %(filename)s %("
                                              "funcName)s %(lineno)s")
    my_new_logger.add_console_handler(log_format="%(name)s %(msg)s", level=logging.CRITICAL)

    my_new_logger.critical("A critical message")
    my_new_logger.debug("debugging message")

