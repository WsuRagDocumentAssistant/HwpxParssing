#================================================
# manifest_parse.py
#================================================

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from xml.etree import ElementTree as ET

from hwpx_parser.model.models.manifest import Manifest, ManifestItem

if TYPE_CHECKING:
    from hwpx_parser.parser.hwpx_parser import HwpxParser

#────────────────────────────────────────────────

_NS = "http://www.idpf.org/2007/opf/"

def _to_item(el: ET.Element) -> ManifestItem:
    return ManifestItem(
        id         = el.get("id", ""),
        href       = el.get("href", ""),
        media_type = el.get("media-type", ""),
        is_embeded = el.get("isEmbeded", "0") == "1",
    )

def parse(parser: HwpxParser) -> Optional[Manifest]:
    if not parser._CONTENT_PATH:
        return None

    root = ET.parse(parser._CONTENT_PATH).getroot()
    items = [
        _to_item(el)
        for el in root.findall(f"{{{_NS}}}manifest/{{{_NS}}}item")
    ]

    manifest = Manifest()
    for item in items:
        if item.media_type.startswith("image/"):
            manifest.images.append(item)
        elif item.id.startswith("section"):
            manifest.sections.append(item)
        elif item.id.startswith("masterpage"):
            manifest.masterpages.append(item)
        elif item.id == "header":
            manifest.header = item
        elif item.id == "settings":
            manifest.settings = item

    return manifest
