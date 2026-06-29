#================================================
# metadata_parse.py
#================================================

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from xml.etree import ElementTree as ET

from hwpx_parser.model.models.metadata import Metadata

if TYPE_CHECKING:
    from hwpx_parser.parser.hwpx_parser import HwpxParser

#────────────────────────────────────────────────

_NS = "http://www.idpf.org/2007/opf/"

def _meta(root: ET.Element, name: str) -> Optional[str]:
    el = root.find(f"{{{_NS}}}metadata/{{{_NS}}}meta[@name='{name}']")
    if el is None:
        return None
    text = el.text
    return text.strip() if text else None

def parse(parser: HwpxParser) -> Optional[Metadata]:
    if not parser._CONTENT_PATH:
        return None

    tree = ET.parse(parser._CONTENT_PATH)
    root = tree.getroot()

    return Metadata(
        creator      = _meta(root, "creator"),
        subject      = _meta(root, "subject"),
        description  = _meta(root, "description"),
        last_save_by = _meta(root, "lastsaveby"),
        created_date = _meta(root, "CreatedDate"),
        modifie_date = _meta(root, "ModifiedDate"),
        date         = _meta(root, "date"),
        keyword      = _meta(root, "keyword"),
    )