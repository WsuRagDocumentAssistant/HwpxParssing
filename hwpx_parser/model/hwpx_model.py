#================================================
# hwpx_model.py
#================================================

from dataclasses import dataclass
from typing import Optional

from .metadata import Metadata

#────────────────────────────────────────────────

@dataclass
class HwpxModel:
    metadata : Optional[Metadata]
