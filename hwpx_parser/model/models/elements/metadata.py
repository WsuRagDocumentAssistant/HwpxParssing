#================================================
# metadata.py
#================================================

from dataclasses import dataclass
from typing import Optional

from hwpx_parser.model.base import HwpxBaseModel

#────────────────────────────────────────────────

@dataclass
class Metadata(HwpxBaseModel):
    creator      : Optional[str]
    subject      : Optional[str]
    description  : Optional[str]
    last_save_by : Optional[str]
    created_date : Optional[str]
    modifie_date : Optional[str]
    date         : Optional[str]
    keyword      : Optional[str]

    def print(self) -> None:
        print("[Metadata]")
        print(f"  creator      : {self.creator}")
        print(f"  subject      : {self.subject}")
        print(f"  description  : {self.description}")
        print(f"  last_save_by : {self.last_save_by}")
        print(f"  created_date : {self.created_date}")
        print(f"  modifie_date : {self.modifie_date}")
        print(f"  date         : {self.date}")
        print(f"  keyword      : {self.keyword}")
        