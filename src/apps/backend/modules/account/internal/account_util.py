import bcrypt


class AccountUtil:
  @staticmethod
  def hash_password(*, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()

  @staticmethod
  def compare_password(*, password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
      hashed_password.encode("utf-8"),
      password.encode("utf-8")
    )
