#================================================
# table_block.py
#================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from .base_block import BaseBlock
from .block_type import BlockType

#------------------------------------------------

@dataclass
class TableBlock(BaseBlock):
    rows: list[list[BaseBlock | None]] = field(default_factory=list)
    width: Optional[int] = None
    height: Optional[int] = None

    def __post_init__(self) -> None:
        self.block_type = BlockType.TABLE
        super().__post_init__()

    def get_width(self) -> Optional[int]:
        return self.width

    def get_height(self) -> Optional[int]:
        return self.height

    def get_content(self) -> list[list[BaseBlock | None]]:
        return self.rows
