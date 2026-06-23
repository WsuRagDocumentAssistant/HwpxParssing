#================================================
# block_registry.py
#================================================

from __future__ import annotations

from typing import Any
import xml.etree.ElementTree as ET

from .base_parser import BaseParser
from .xml_utils import local_name

#------------------------------------------------

class BlockRegistry:
    _parsers: dict[str, type[BaseParser]] = {}

    @classmethod
    def register(cls, tag_name: str, parser_cls: type[BaseParser]) -> None:
        """태그 이름과 파서 클래스를 등록하는 함수"""
        cls._parsers[tag_name] = parser_cls

    @classmethod
    def parse(cls, source: ET.Element, **kwargs: Any) -> Any:
        """등록된 파서 클래스를 찾아서 해당 XML 태그를 파싱하는 함수"""
        parser_cls = cls._parsers.get(local_name(source.tag))
        if parser_cls is None:
            return None

        return parser_cls.parse(source, **kwargs)
