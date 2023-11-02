from abc import ABC, abstractmethod


class BaseLogger(ABC):
  @staticmethod
  @abstractmethod
  def critical(*, message: str) -> None:
    ...

  @staticmethod
  @abstractmethod
  def debug(*, message: str) -> None:
    ...

  @staticmethod
  @abstractmethod
  def error(*, message: str) -> None:
    ...

  @staticmethod
  @abstractmethod
  def info(*, message: str) -> None:
    ...

  @staticmethod
  @abstractmethod
  def warn(*, message: str) -> None:
    ...
