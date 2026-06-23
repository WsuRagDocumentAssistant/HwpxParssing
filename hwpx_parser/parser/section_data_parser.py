#================================================
# section_data_parser.py
#================================================

from __future__ import annotations

from pathlib import Path
from typing import Any
# 정규표현식 라이브러리, 파일 이름에서 section 번호를 추출하는 데 사용
import re
# XML 파일을 읽고 태그를 분석하기 위한 파이썬 기본 라이브러리
import xml.etree.ElementTree as ET

# 본문 파싱 결과를 담는 BaseBlock 클래스
from ..blocks.base_block import BaseBlock
# 공통 파서 부모 클래스
from .base_parser import BaseParser
# 각 XML 태그를 어떤 파서가 처리할지 연결해주는 등록소
from .block_registry import BlockRegistry
# 헤더 정보 파싱 클래스
from .header_parser import HeaderParser
# 문단, 이미지, 표를 파싱하는 클래스 등록
from .image_parser import ImageParser
from .paragraph_parser import ParagraphParser
from .table_parser import TableParser
# section 파싱할 때 필요한 공통 정보를 담는 객체
from .section_context import SectionParseContext
# XML 태그 이름에서 네임스페이스를 제거하고 실제 태그명만 가져오는 함수
from .xml_utils import local_name

#------------------------------------------------

class SectionParser(BaseParser):

    # section XML 네임스페이스 설정, 현재 코드에서는 cls.NS를 직접 쓰지는 않음
    NS: dict[str, str] = {
        "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    }

    @classmethod
    def parse(
        cls,
        section_sources: list[str | Path],
        **kwargs: Any,
    ) -> list[BaseBlock]:
        """
        section XML 파일 여러 개를 받아서 본문 블록 리스트를 반환
        section_sources : section XML 파일 경로 리스트
        kwargs : header_source, image_dir_path 같은 추가 정보
            - header_source : header.xml 파일 경로
            - image_dir_path : 이미지 파일이 저장된 폴더 경로
        """

        header_source = kwargs.get("header_source")
        image_dir_path = kwargs.get("image_dir_path")
        # header_source, image_dir_path 검사, 둘중 하나라도 없으면 예외 발생
        if header_source is None or image_dir_path is None:
            raise ValueError("header_source and image_dir_path are required")

        """
        context
        ├── header
        │   └── header.xml을 분석한 결과
        │       ├── para_pr_to_level
        │       ├── style_to_para_pr
        │       └── style_names
        │
        └── image_dir_path
            └── 이미지 파일이 저장된 폴더 경로
        """
        # context 생성
        context = SectionParseContext(
            # header.xml을 파싱한 결과
            header=HeaderParser.parse(str(header_source)),
            # 이미지 파일이 저장된 폴더 경로
            image_dir_path=Path(image_dir_path),
        )

        # 최상위 부모 역할을 하는 가짜 루트 블록 생성
        root_block = BaseBlock()
        # 제목/문단의 계층을 만들기 위한 리스트
        stack: list[tuple[int, BaseBlock]] = [(-1, root_block)]

        # section 파일들을 정렬해서 순서대로 처리
        for section_source in cls._sort_section_sources(section_sources):
            # XML 트리 생성
            tree = ET.parse(str(section_source))
            # 루트 노드 가져오기
            root = tree.getroot()

            # section XML의 최상위 자식들을 하나씩 확인
            for child in list(root):
                # 태그 이름만 추출
                tag = local_name(child.tag)
                # 필요한 태그만 처리 - 문단, 표, 이미지
                if tag not in {"p", "tbl", "pic"}:
                    continue

                # BlockRegistry를 통해 적절한 파서를 찾아서 블록 생성
                block = BlockRegistry.parse(child, context=context)
                # 파싱 결과가 None이면 건너뛰기
                if block is None:
                    continue

                # 추가: section XML 요소의 styleIDRef / paraPrIDRef를 기준으로 level 부여
                cls._apply_outline_level(child, block, context)

                # 블록을 계층에 붙이기
                cls._attach_block(stack, block)

        # 가짜 루트 블록의 자식들만 반환
        return root_block.children


    @classmethod
    def _apply_outline_level(
        cls,
        node: ET.Element,
        block: BaseBlock,
        context: SectionParseContext,
    ) -> None:
        style_id = node.attrib.get("styleIDRef")
        para_pr_id = node.attrib.get("paraPrIDRef")

        level = context.header.get_outline_level(
            para_pr_id=para_pr_id,
            style_id=style_id,
        )

        if level is not None:
            block.level = level

    @classmethod
    def _attach_block(cls, stack: list[tuple[int, BaseBlock]], block: BaseBlock) -> None:
        """
        파싱된 블록을 현재 계층 구조에 붙이는 함수
        """

        # block 객체에 level이라는 속성이 있는지 확인
        level = getattr(block, "level", None)

        # level이 int면 제목/계층 블록으로 처리
        if isinstance(level, int):
            while len(stack) > 1 and stack[-1][0] >= level:
                stack.pop()

            # 현재 stack의 마지막 블록이 새 블록의 부모
            stack[-1][1].add_child(block)
            # 새 블록을 stack에 추가하여 계층 구조 유지
            stack.append((level, block))
            return

        # level이 없는 일반 문단이면 현재 부모 밑에 추가
        stack[-1][1].add_child(block)

    @classmethod
    def _sort_section_sources(cls, section_sources: list[str | Path]) -> list[str | Path]:
        """section 파일들을 정렬"""
        return sorted(section_sources, key=cls._section_sort_key)

    @classmethod
    def _section_sort_key(cls, source: str | Path) -> tuple[int, str]:
        """파일 이름에서 section 번호를 뽑아 정렬 기준으로 만드는 함수"""
        source_path = Path(source)
        match = re.search(r"section(\d+)\.xml$", source_path.name)
        if match is None:
            return (10**9, source_path.name)

        return (int(match.group(1)), source_path.name)
