#================================================
# image_parser.py
#================================================

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Any

from ..blocks.image_block import ImageBlock
from .base_parser import BaseParser
from .block_registry import BlockRegistry
from .xml_utils import local_name, parse_int, split_lines

#------------------------------------------------

class ImageParser(BaseParser):
    NS: dict[str, str] = {
        "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    }

    @classmethod
    def parse(cls, source: ET.Element, **kwargs: Any) -> ImageBlock:
        context = kwargs.get("context")

        binary_item_id_ref = cls._get_binary_item_id_ref(source)
        image_path = cls._resolve_image_path(binary_item_id_ref, context)
        width, height = cls._get_image_dimension(source)
        title, contents = cls._get_comment_text(source)

        block = ImageBlock(
            image_name=binary_item_id_ref,
            binary_item_id_ref=binary_item_id_ref,
            width=width,
            height=height,
            image_path=image_path,
        )
        block.set_text(title, contents)
        return block

    @classmethod
    def _get_binary_item_id_ref(cls, source: ET.Element) -> str | None:
        for child in source.iter():
            if local_name(child.tag) == "img":
                return child.attrib.get("binaryItemIDRef")
        return None

    @classmethod
    def _resolve_image_path(cls, image_name: str | None, context: Any) -> str | None:
        if image_name is None or context is None:
            return None

        image_dir_path = Path(context.image_dir_path)
        for candidate in sorted(image_dir_path.glob(f"{image_name}.*")):
            return str(candidate)

        return None

    @classmethod
    def _get_image_dimension(cls, source: ET.Element) -> tuple[int | None, int | None]:
        width = None
        height = None

        for child in source.iter():
            tag = local_name(child.tag)
            if tag in {"orgSz", "sz"}:
                width = parse_int(child.attrib.get("width"))
                height = parse_int(child.attrib.get("height"))
                if width is not None or height is not None:
                    return width, height

        return width, height

    @classmethod
    def _get_comment_text(cls, source: ET.Element) -> tuple[str | None, str | None]:
        for child in source.iter():
            if local_name(child.tag) == "shapeComment":
                lines = split_lines(child.text)
                if not lines:
                    return None, None

                title = lines[0]
                contents = "\n".join(lines[1:]) if len(lines) > 1 else None
                return title, contents

        return None, None


BlockRegistry.register("pic", ImageParser)
