#================================================
# base_parser.py
#================================================

from __future__ import annotations

# 추상 클래스를 만들기 위한 import , ABc - 추상 클래스의 부모, abstractmethod - 반드시 자식 클래스에서 구현해야 하는 메서드 표시
from abc import ABC, abstractmethod
from typing import Any

#------------------------------------------------

class BaseParser(ABC):
    """
    모든 Parser 클래스가 반드시 parse() 메서드를 가지도록 강제하는 부모 클래스
    """
    @classmethod # 이 메서드는 객체를 만들지 않고 클래스 이름으로 호출할 수 있다는 뜻
    @abstractmethod
    def parse(cls, source: Any, **kwargs: Any) -> Any:
        pass
