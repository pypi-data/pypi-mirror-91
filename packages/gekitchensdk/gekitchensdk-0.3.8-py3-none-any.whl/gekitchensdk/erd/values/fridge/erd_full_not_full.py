import enum
from typing import Optional

@enum.unique
class ErdFullNotFull(enum.Enum):
    FULL = "01"
    NOT_FULL = "00"
    NA = "NA"

    def boolify(self) -> Optional[bool]:
        if self.value == ErdFullNotFull.NA:
            return None
        return self.value == ErdFullNotFull.FULL