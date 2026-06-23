#================================================
# table_parser.py
#================================================

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

from ..blocks.paragraph_block import ParagraphBlock
from ..blocks.table_block import TableBlock
from .base_parser import BaseParser
from .block_registry import BlockRegistry
from .xml_utils import local_name, parse_int

#------------------------------------------------

class TableParser(BaseParser):
    NS: dict[str, str] = {
        "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    }

    @classmethod
    def parse(cls, source: ET.Element, **kwargs: Any) -> TableBlock:
        context = kwargs.get("context")

        table = TableBlock(
            width=cls._get_table_dimension(source, "width"),
            height=cls._get_table_dimension(source, "height"),
        )

        for child in list(source):
            if local_name(child.tag) != "tr":
                continue

            row: list[Any] = []
            for cell_node in list(child):
                if local_name(cell_node.tag) != "tc":
                    continue

                row.append(cls._parse_cell(cell_node, context))

            if row:
                table.rows.append(row)

        return table

    @classmethod
    def _parse_cell(cls, source: ET.Element, context: Any) -> ParagraphBlock | TableBlock | None:
        sub_list = None
        for child in list(source):
            if local_name(child.tag) == "subList":
                sub_list = child
                break

        if sub_list is None:
            return None

        blocks: list[Any] = []
        for child in list(sub_list):
            tag = local_name(child.tag)
            if tag in {"p", "tbl", "pic"}:
                parsed = BlockRegistry.parse(child, context=context)
                if parsed is not None:
                    blocks.append(parsed)

        if not blocks:
            return None

        if len(blocks) == 1:
            return blocks[0]

        wrapper = ParagraphBlock()
        for block in blocks:
            wrapper.add_child(block)
        return wrapper

    @classmethod
    def _get_table_dimension(cls, source: ET.Element, key: str) -> int | None:
        dimension_node = None
        for child in list(source):
            if local_name(child.tag) == "sz":
                dimension_node = child
                break

        if dimension_node is None:
            return None

        return parse_int(dimension_node.attrib.get(key))


BlockRegistry.register("tbl", TableParser)
