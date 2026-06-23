#================================================
# base_block.py
#================================================

from __future__ import annotations

from abc import ABC
# 리스트처럼 기본값을 조심해서 만들어야 하는 필드에 사용
from dataclasses import dataclass, field
from typing import Optional

# 블록이 문단인지, 제목인지, 표인지 구분하기 위한 타입
from .block_type import BlockType

#------------------------------------------------

def split_sentences(contents: str | None) -> list[str]:
    """
    문단 내용을 문장 단위로 나누는 함수
    """
    if not contents:
        return []

    # 여러 줄로 된 문자열을 한 줄로 정리하는 코드
    normalized = " ".join(part.strip() for part in contents.splitlines() if part.strip())
    # 줄바꿈과 공백을 제거했더니 실제 내용이 없으면 빈 리스트 반환
    if not normalized:
        return []

    # 문장 저장용 변수
    # 완성된 문장들을 담는 리스트
    sentences: list[str] = []
    # 현재 읽고 있는 문장
    current = ""
    # 문장 끝으로 판단할 문자들
    sentence_endings = ".!?。！？"

    # 문장 단위로 나누는 코드
    for char in normalized:
        current += char
        if char in sentence_endings:
            cleaned = current.strip()
            if cleaned:
                sentences.append(cleaned)
            current = ""

    cleaned = current.strip()
    if cleaned:
        sentences.append(cleaned)

    if not sentences and normalized:
        sentences.append(normalized)

    # 최종적으로 문장 리스트를 반환
    return sentences


@dataclass
class BaseBlock(ABC):
    """
    모든 블록 클래스가 상속받는 기본 클래스
    블록 종류 저장
    제목 저장
    본문 내용 저장
    문장 목록 저장
    자식 블록 저장
    """

    # 블록 종류 저장, 기본값은 문단
    block_type: BlockType = BlockType.PARAGRAPH
    # 제목 저장, 기본값은 None
    title: Optional[str] = None
    # 본문 내용 저장, 기본값은 None
    contents: Optional[str] = None
    # 문장 목록 저장, 기본값은 빈 리스트
    sentences: list[str] = field(default_factory=list)
    # 자식 블록 저장, 기본값은 빈 리스트
    children: list[BaseBlock] = field(default_factory=list)

    # dataclass에서 객체 생성이 끝난 직후 자동으로 실행되는 메서드
    def __post_init__(self) -> None:
        """
        contents가 있고,
        sentences가 아직 비어 있으면,
        contents를 문장 단위로 나눠서 sentences에 저장한다.
        """
        if self.contents and not self.sentences:
            self.sentences = split_sentences(self.contents)

    # 현재 블록에 자식 블록을 추가하는 메서드
    def add_child(self, block: BaseBlock) -> None:
        self.children.append(block)

    # getter 메서드들
    # 현재 블록의 제목을 반환
    def get_title(self) -> Optional[str]:
        return self.title

    # 현재 블록의 본문 내용을 반환
    def get_contents(self) -> Optional[str]:
        return self.contents

    # 현재 블록의 문장 목록을 반환
    def get_sentences(self) -> list[str]:
        return self.sentences

    # 현재 블록의 자식 블록 목록을 반환
    def get_child(self) -> list[BaseBlock]:
        return self.children

    # setter 메서드들
    # 블록의 제목과 본문을 나중에 변경하는 메서드
    
    def get_children(self) -> list[BaseBlock]:
        return self.children

    def set_text(self, title: Optional[str], contents: Optional[str]) -> None:
        self.title = title
        self.contents = contents
        self.sentences = split_sentences(contents)
