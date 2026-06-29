#================================================
# base.py
#================================================

from abc import ABC, abstractmethod

#────────────────────────────────────────────────

class HwpxBaseModel(ABC):
    @abstractmethod
    def print(self) -> None: ...
