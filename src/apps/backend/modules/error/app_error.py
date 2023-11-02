from typing import Any


class AppError(Exception):
  def __init__(self, message: str, status_code: int) -> None:
    self.message = message
    self.status_code = status_code
    super().__init__(self.message)

  def to_str(self) -> str:
    return f"{self.status_code}: {self.message}"

  def to_dict(self) -> dict[str, Any]:
    error_dict = {
      'message': self.message,
      'status_code': self.status_code,
      'args': self.args,
      'with_traceback': self.with_traceback
    }
    return error_dict
