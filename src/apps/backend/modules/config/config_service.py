class ConfigService:
  @staticmethod
  def get_bool_value(key: str) -> bool:
    ...

  @staticmethod
  def get_int_value(key: str) -> int:
    ...

  @staticmethod
  def get_string_value(key: str) -> str:
    ...

  @staticmethod
  def get_list_value(key: str) -> list:
    ...

  @staticmethod
  def has_value(key: str) -> bool:
    ...

  @staticmethod
  def get_value(expected_value_type: type, key: str) -> type:
    ...

