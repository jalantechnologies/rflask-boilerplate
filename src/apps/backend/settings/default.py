from dataclasses import dataclass


@dataclass(frozen=True)
class DefaultSettings:
  SERVER_PORT: int = 8080
  WEB_APP_HOST: str = "http://localhost:3000"
