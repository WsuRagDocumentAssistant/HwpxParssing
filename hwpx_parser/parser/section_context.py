#================================================
# section_context.py
# section0.xml, section1.xml을 분석할 때 필요한 header.xml 참조 정보와 이미지 폴더 경로를 한 곳에 묶어서 전달
#================================================

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

#------------------------------------------------

@dataclass
class HeaderContext:
    """header.xml에서 읽어온 참조 정보를 저장하는 클래스"""

    # paraPrIDRef가 어떤 개요 레벨인지 저장하는 딕셔너리
    para_pr_to_level: dict[str, int] = field(default_factory=dict) # 빈 딕셔너리를 기본값
    # styleIDRef가 어떤 paraPrIDRef를 가리키는지 저장하는 딕셔너리
    style_to_para_pr: dict[str, str] = field(default_factory=dict)
    # styleIDRef가 어떤 스타일 이름인지 저장하는 딕셔너리
    style_names: dict[str, str] = field(default_factory=dict)

    def get_outline_level(self, para_pr_id: str | None, style_id: str | None) -> Optional[int]:
        """
        문단의 paraPrIDRef 또는 styleIDRef를 보고
        해당 문단이 몇 단계 제목인지 반환하는 함수
        """

        # 1순위: section 문단에 직접 붙은 paraPrIDRef로 먼저 level 확인
        if para_pr_id is not None:
            level = self.para_pr_to_level.get(para_pr_id)
            if level is not None:
                return level

        # 2순위: styleIDRef가 가리키는 paraPrIDRef로 level 확인
        if style_id is not None:
            mapped_para_pr = self.style_to_para_pr.get(style_id)
            if mapped_para_pr is not None:
                return self.para_pr_to_level.get(mapped_para_pr)

        return None


@dataclass
class SectionParseContext:
    """section XML을 파싱할 때 필요한 전체 context"""

    # header.xml에서 읽은 스타일/문단 참조 정보
    header: HeaderContext
    # 이미지가 저장된 폴더 경로
    image_dir_path: Path
