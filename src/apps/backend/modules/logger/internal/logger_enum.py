import logging 
from enum import Enum 

class Levels(Enum):
    debug = ["debug",logging.DEBUG]
    info  = ["info",logging.INFO]
    warning = ["warning",logging.WARNING]
    error = ["error",logging.ERROR]
    critical = ["critical",logging.CRITICAL]
    
