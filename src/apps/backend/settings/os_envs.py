import os
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class OSSettings:
  INSPECTLET_KEY: Optional[str] = os.environ.get("INSPECTLET_KEY")
  MONGODB_URI: Optional[str] = os.environ.get("MONGODB_URI")
  PAPERTRAIL_HOST: Optional[str] = os.environ.get("PAPERTRAIL_HOST")
  PAPERTRAIL_PORT: Optional[str] = os.environ.get("PAPERTRAIL_PORT")
  WEB_APP_HOST: Optional[str] = os.environ.get("WEB_APP_HOST")
