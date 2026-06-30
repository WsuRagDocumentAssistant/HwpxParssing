#================================================
# manifest.py
#================================================

from dataclasses import dataclass, field
from typing import Optional

from hwpx_parser.model.base import HwpxBaseModel

#────────────────────────────────────────────────

@dataclass
class ManifestItem(HwpxBaseModel):
    id         : str
    href       : str
    media_type : str
    is_embeded : bool = False

    def print(self) -> None:
        print(f"    [{self.id}] {self.href} ({self.media_type})" + (" *embedded" if self.is_embeded else ""))

@dataclass
class Manifest(HwpxBaseModel):
    images      : list[ManifestItem] = field(default_factory=list)
    sections    : list[ManifestItem] = field(default_factory=list)
    masterpages : list[ManifestItem] = field(default_factory=list)
    header      : Optional[ManifestItem] = None
    settings    : Optional[ManifestItem] = None

    def print(self) -> None:
        print("[Manifest]")
        print(f"  images ({len(self.images)})")
        for item in self.images:
            item.print()
        print(f"  sections ({len(self.sections)})")
        for item in self.sections:
            item.print()
        print(f"  masterpages ({len(self.masterpages)})")
        for item in self.masterpages:
            item.print()
        print(f"  header      : ", end=""); self.header.print() if self.header else print(None)
        print(f"  settings    : ", end=""); self.settings.print() if self.settings else print(None)
