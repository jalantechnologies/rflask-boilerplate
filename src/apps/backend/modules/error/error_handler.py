class MissingKeyError(Exception):
  def __init__(self, *, missing_key: str, error_code: str) -> None:
    super().__init__(f"{missing_key} is not found")
    self.code = error_code


class ValueTypeMismatchError(Exception):
  def __init__(self, *, actual_value_type: str, error_code: str, expected_value_type: str, key: str):
    super().__init__(
      f"Value mismatch for key: {key}. Expected: {expected_value_type}, Actual: {actual_value_type}"
    )
    self.code = error_code
