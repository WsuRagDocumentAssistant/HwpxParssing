#================================================
# header_parser.py
#================================================

from __future__ import annotations

import xml.etree.ElementTree as ET

from .base_parser import BaseParser
from .section_context import HeaderContext

#------------------------------------------------

class HeaderParser(BaseParser):
    """header.xml을 파싱하는 클래스"""

    # 네임스페이스 설정
    NS: dict[str, str] = {
        "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    }

    @classmethod
    def parse(cls, source: str, **kwargs) -> HeaderContext:
        """header.xml 파일 경로를 받아서 HeaderContext 객체를 반환"""

        # XML 파일 읽기
        tree = ET.parse(source)
        root = tree.getroot()

        # 빈 HeaderContext 객체 생성
        context = HeaderContext()

        # header.xml 안에 있는 모든 <hh:paraPr> 태그를 찾는 부분
        for para_node in root.findall(".//hh:paraPr", cls.NS):
            # paraPr id 가져오기
            para_pr_id = para_node.attrib.get("id")
            # heading 태그 찾기
            heading_node = para_node.find("hh:heading", cls.NS)
            # id나 heading이 없으면 건너뜀
            # 그 문단 설정은 제목 레벨 판단에 쓸 수 없으니까 넘어간다.
            if para_pr_id is None or heading_node is None:
                continue

            # OUTLINE인 경우만 저장
            if heading_node.attrib.get("type") == "OUTLINE":
                # level 숫자로 바꾼 뒤 저장
                level = heading_node.attrib.get("level")
                if level is not None:
                    context.para_pr_to_level[para_pr_id] = int(level)

        # header.xml 안에 있는 모든 <hh:style> 태그를 찾는 부분
        for style_node in root.findall(".//hh:style", cls.NS):
            # style id와 paraPrIDRef 가져오기
            style_id = style_node.attrib.get("id")
            para_pr_id = style_node.attrib.get("paraPrIDRef")
            if style_id is None or para_pr_id is None:
                continue

            # style id → paraPr id 저장
            context.style_to_para_pr[style_id] = para_pr_id
            style_name = style_node.attrib.get("name")
            if style_name is not None:
                context.style_names[style_id] = style_name

        # 파싱한 결과가 담긴 HeaderContext를 반환
        return context
