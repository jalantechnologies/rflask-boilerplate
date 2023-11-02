from modules.logger.internal.console_logger import ConsoleLogger


class Loggers:
  _loggers = []

  @staticmethod
  def initialize_loggers() -> None:
    ...

  @staticmethod
  def info(*, message: str) -> None:
    [logger.info(message) for logger in Loggers._loggers]

  @staticmethod
  def debug(*, message: str) -> None:
    [logger.debubg(message) for logger in Loggers._loggers]

  @staticmethod
  def error(*, message: str) -> None:
    [logger.error(message) for logger in Loggers._loggers]

  @staticmethod
  def warn(*, message: str) -> None:
    [logger.warn(message) for logger in Loggers._loggers]

  @staticmethod
  def critical(*, message: str) -> None:
    [logger.critical(message) for logger in Loggers._loggers]
