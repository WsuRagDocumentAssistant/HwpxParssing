#================================================
# xml_utils.py
#================================================

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

#------------------------------------------------

# 네임스페이스를 제거하고 실제 태그 이름만 가져오는 함수
def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


# 텍스트 안에 있는 줄바꿈 문자를 공백으로 바꿔서 한 줄 텍스트로 정리하는 함수
def normalize_text(text: str | None) -> str:
    if text is None:
        return ""
    return text.replace("\r", " ").replace("\n", " ")


# 문자열을 정수로 바꾸는 함수
def parse_int(value: str | None) -> int | None:
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None

# 텍스트를 줄 단위로 나누고, 빈 줄은 제거하는 함수
def split_lines(text: str | None) -> list[str]:
    if not text:
        return []

    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


# 텍스트를 문장 단위로 나누는 함수
def split_sentences(text: str | None) -> list[str]:
    if not text:
        return []

    normalized = " ".join(part.strip() for part in text.splitlines() if part.strip())
    if not normalized:
        return []

    chunks = re.split(r"(?<=[.!?。！？])\s+", normalized)
    sentences = [chunk.strip() for chunk in chunks if chunk.strip()]
    return sentences or [normalized]
