# ./app/enums.py
from enum import Enum

class UserStatus(Enum):
    NOT_INVITED = "NOT_INVITED"
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    REMOVED = "REMOVED"
    