from modules.logger.internal.base_logger import BaseLogger


class ConsoleLogger(BaseLogger):
  @staticmethod
  def critical(*, message: str) -> None:
    print(message)

  @staticmethod
  def debug(*, message: str) -> None:
    print(message)

  @staticmethod
  def error(*, message: str) -> None:
    print(message)

  @staticmethod
  def info(*, message: str) -> None:
    print(message)

  @staticmethod
  def warn(*, message: str) -> None:
    print(message)
