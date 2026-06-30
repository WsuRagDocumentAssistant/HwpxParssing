#================================================
# header_parse.py
#================================================

from __future__ import annotations

from typing import TYPE_CHECKING
from xml.etree import ElementTree as ET

from hwpx_parser.model.models.elements.style import Style

if TYPE_CHECKING:
    from hwpx_parser.parser.hwpx_parser import HwpxParser

#────────────────────────────────────────────────

_NS = "http://www.hancom.co.kr/hwpml/2011/head"

def _build_level_map(root: ET.Element) -> dict[int, int]:
    level_map = {}
    for para_pr in root.findall(f"{{{_NS}}}refList/{{{_NS}}}paraProperties/{{{_NS}}}paraPr"):
        id_     = int(para_pr.get("id", "0"))
        heading = para_pr.find(f"{{{_NS}}}heading")
        level   = int(heading.get("level", "0")) if heading is not None else 0
        level_map[id_] = level
    return level_map

def parse(parser: HwpxParser) -> list[Style]:
    if not parser._HEADER_PATH:
        return []

    root      = ET.parse(parser._HEADER_PATH).getroot()
    level_map = _build_level_map(root)

    return [
        Style(
            id       = int(el.get("id", "0")),
            type     = el.get("type", ""),
            name     = el.get("name", ""),
            eng_name = el.get("engName", ""),
            level    = level_map.get(int(el.get("paraPrIDRef", "0")), 0),
        )
        for el in root.findall(f"{{{_NS}}}refList/{{{_NS}}}styles/{{{_NS}}}style")
    ]
