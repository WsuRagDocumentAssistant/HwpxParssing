#================================================
# metadata.py
#================================================

from dataclasses import dataclass
from typing import Optional

#------------------------------------------------

@dataclass
class Metadata:
    """메타 데이터 저장 객체"""
    title :         Optional[str] = None
    creator :       Optional[str] = None
    subject :       Optional[str] = None
    description :   Optional[str] = None
    last_save_by :  Optional[str] = None
    created_date :  Optional[str] = None
    modified_date : Optional[str] = None
    date :          Optional[str] = None
    keyword :       Optional[str] = None