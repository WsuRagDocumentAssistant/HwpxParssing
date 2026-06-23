#================================================
# paragraph_block.py
#================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base_block import BaseBlock
from .block_type import BlockType

#------------------------------------------------

@dataclass
class ParagraphBlock(BaseBlock):
    level: Optional[int] = None
    para_pr_id: Optional[str] = None
    style_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.block_type = BlockType.PARAGRAPH
        super().__post_init__()
