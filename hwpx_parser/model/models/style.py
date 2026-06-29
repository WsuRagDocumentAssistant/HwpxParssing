#================================================
# style.py
#================================================

from dataclasses import dataclass

from hwpx_parser.model.base import HwpxBaseModel

#────────────────────────────────────────────────

@dataclass
class Style(HwpxBaseModel):
    id       : int
    type     : str
    name     : str
    eng_name : str
    level    : int

    def print(self) -> None:
        print(f"    [{self.id:>3}] ({self.type:<4}) lv.{self.level}  {self.name} / {self.eng_name}")