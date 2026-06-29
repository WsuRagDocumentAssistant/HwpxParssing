#================================================
# hwpx_parser.py
#================================================

from __future__ import annotations

from typing import Optional
from pathlib import Path
import zipfile

from ..model.hwpx_model import HwpxModel
from .parsers import metadata_parse
from .parsers import manifest_parse
from .parsers import header_parse

#────────────────────────────────────────────────


class HwpxParser:
    """
    document_path : 문서의 경로
    unpacked_path : 압축해제할 경로
    """
    def __init__(self, document_path:str, unpacked_path : str):
        self._ROOT              = Path(document_path)
        self._FILENAME          = self._ROOT.stem
        self._UNPACKED_DIR_PATH = Path(unpacked_path) / "unpacked" / self._FILENAME

        self._CONTENT_PATH = self._UNPACKED_DIR_PATH / "Contents" / "content.hpf"
        self._HEADER_PATH  = self._UNPACKED_DIR_PATH / "Contents" / "header.xml"

        self.hwpx = HwpxModel()
        self.__unpack_hwpx()


    def __call__(self):
        self.parse()


    def parse(self) -> Optional[HwpxModel]:
        self.hwpx.metadata = metadata_parse.parse(self)
        self.hwpx.manifest = manifest_parse.parse(self)
        self.hwpx.styles   = header_parse.parse(self)
        return self.hwpx


    def __unpack_hwpx(self) -> None:
        if self._UNPACKED_DIR_PATH.exists(): return
        self._UNPACKED_DIR_PATH.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(self._ROOT, "r") as zip_ref:
            zip_ref.extractall(self._UNPACKED_DIR_PATH)
    