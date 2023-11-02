from modules.logger.internal.loggers import Loggers


class Logger:
  @staticmethod
  def critical(*, message: str) -> None:
    Loggers.critical(message)

  @staticmethod
  def info(*, message: str) -> None:
    Loggers.info(message)

  @staticmethod
  def debug(*, message: str) -> None:
    Loggers.debug(message)

  @staticmethod
  def error(*, message: str) -> None:
    Loggers.error(message)

  @staticmethod
  def warn(*, message: str) -> None:
    Loggers.warn(message)
