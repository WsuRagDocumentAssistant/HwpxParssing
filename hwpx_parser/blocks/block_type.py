#================================================
# block_type.py
#================================================

from enum import StrEnum

#------------------------------------------------

class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    TABLE = "table"
    IMAGE = "image"
