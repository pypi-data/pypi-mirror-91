from logging import Logger

class LoggerWrapper:
    """
    This services allows the notebook-scoped logger to be lazy-loaded
    """

    def __init__(
        self,
        logger: Logger,
    ):
        self.__logger = logger

    def getLogger(self):
        return self.__logger
