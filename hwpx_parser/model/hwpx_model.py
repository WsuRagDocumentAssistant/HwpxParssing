#================================================
# hwpx_model.py
#================================================

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .models.metadata import Metadata
from .models.manifest import Manifest
from .models.style import Style

#────────────────────────────────────────────────

@dataclass
class HwpxModel:
    metadata : Optional[Metadata]   = None
    manifest : Optional[Manifest]   = None
    styles   : list[Style]          = None

    def print(self) -> None:
        if self.metadata: self.metadata.print()
        if self.manifest: self.manifest.print()
        if self.styles:
            print(f"[Styles] ({len(self.styles)})")
            for style in self.styles:
                style.print()