#================================================
# image_block.py
#================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .base_block import BaseBlock
from .block_type import BlockType

#------------------------------------------------

@dataclass
class ImageBlock(BaseBlock):
    image_name: Optional[str] = None
    binary_item_id_ref: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    image_path: Optional[str] = None

    def __post_init__(self) -> None:
        self.block_type = BlockType.IMAGE
        super().__post_init__()

    def get_width(self) -> Optional[int]:
        return self.width

    def get_height(self) -> Optional[int]:
        return self.height

    def get_img_to_byte(self, image_dir_path: str | Path) -> list[int]:
        if not self.binary_item_id_ref:
            return []

        base_path = Path(image_dir_path)
        for candidate in sorted(base_path.glob(f"{self.binary_item_id_ref}.*")):
            return list(candidate.read_bytes())

        return []
