#================================================
# metadata.py
#================================================

# 데이터를 저장하는 클래스를 편하게 만들게 해주는 기능
from dataclasses import dataclass
# Optional은 값이 없을 수도 있다는 의미, 즉 None이 될 수도 있다는 뜻
from typing import Optional

#------------------------------------------------

# Metadata 클래스를 데이터 저장용 클래스로 만들어주는 표시
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