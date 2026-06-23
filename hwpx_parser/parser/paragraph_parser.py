#================================================
# paragraph_parser.py
#================================================

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

from ..blocks.paragraph_block import ParagraphBlock
from .base_parser import BaseParser
from .block_registry import BlockRegistry
from .xml_utils import local_name, normalize_text

#------------------------------------------------

class ParagraphParser(BaseParser):
    NS: dict[str, str] = {
        "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    }

    @classmethod
    def parse(cls, source: ET.Element, **kwargs: Any) -> ParagraphBlock:
        context = kwargs.get("context")

        block = ParagraphBlock(
            para_pr_id=source.attrib.get("paraPrIDRef"),
            style_id=source.attrib.get("styleIDRef"),
        )

        level = None
        if context is not None:
            level = context.header.get_outline_level(
                source.attrib.get("paraPrIDRef"),
                source.attrib.get("styleIDRef"),
            )
        block.level = level

        lines, child_blocks = cls._collect_block_data(source, context)
        clean_lines = [line for line in lines if line]

        if clean_lines:
            title = clean_lines[0]
            contents = "\n".join(clean_lines[1:]) if len(clean_lines) > 1 else None
            block.set_text(title, contents)
        else:
            block.set_text(None, None)

        for child_block in child_blocks:
            block.add_child(child_block)

        return block

    @classmethod
    def _collect_block_data(cls, source: ET.Element, context: Any) -> tuple[list[str], list[Any]]:
        lines: list[str] = []
        current_line: list[str] = []
        child_blocks: list[Any] = []

        def flush_line() -> None:
            line = "".join(current_line).strip()
            if line:
                lines.append(line)
            current_line.clear()

        def append_text(text: str | None) -> None:
            normalized = normalize_text(text)
            if normalized.strip():
                current_line.append(normalized)

        def walk(node: ET.Element) -> None:
            append_text(node.text)

            for child in list(node):
                tag = local_name(child.tag)
                if tag == "lineBreak":
                    flush_line()
                elif tag in {"tbl", "pic"}:
                    parsed = BlockRegistry.parse(child, context=context)
                    if parsed is not None:
                        child_blocks.append(parsed)
                else:
                    walk(child)

                append_text(child.tail)

        walk(source)
        flush_line()

        return lines, child_blocks


BlockRegistry.register("p", ParagraphParser)
