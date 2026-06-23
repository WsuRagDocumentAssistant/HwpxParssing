#================================================
# metadata_parser.py
#================================================

from __future__ import annotations

# 최종 결과를 담을 Metadata 객체
from ..blocks.meta_data import Metadata
from .base_parser import BaseParser

# 부모 클래스의 메서드를 자식 클래스에서 재정의
from typing_extensions import override
# XML 파일을 읽고 파싱하기 위한 파이썬 기본 라이브러리, XML 파일을 읽어서 태그를 찾는 데 사용
import xml.etree.ElementTree as ET
# Any는 타입을 딱 정하지 않겠다는 뜻
from typing import Any

#------------------------------------------------

# MetadataParser는 BaseParser를 상속받는 클래스
class MetadataParser(BaseParser):
    """
    metadata.xml 같은 XML 파일 읽기
    → opf:metadata 태그 찾기
    → 제목과 meta 정보 추출
    → Metadata 객체에 저장
    → Metadata 객체 반환
    """

    # 네임스페이스 설정
    # XML에서 opf: 접두사가 붙은 태그를 찾기 위한 설정
    NS : dict[str,str] = { 
        "opf" : "http://www.idpf.org/2007/opf/" 
    }
    
    # 메타데이터 XML에서 추출할 정보와 Metadata 객체의 속성 이름을 매핑
    META_MAP : dict[str,str] = {
        "creator":      "creator",
        "subject":      "subject",
        "description":  "description",
        "lastsaveby":   "last_save_by",
        "CreatedDate":  "created_date",
        "ModifiedDate": "modified_date",
        "date" :        "date",
        "keyword":      "keyword"
    }

    @override
    @classmethod
    def parse(cls,metadata_source : str, **kwargs: Any) -> Metadata:
        """
        metadata_source 경로에 있는 XML 파일을 읽어서
        Metadata 객체로 변환해서 반환한다.
        """

        # 빈 Metadata 객체 생성
        metadata = Metadata()

        # XML 파일 읽기
        tree = ET.parse(metadata_source)
        # XML 트리의 루트 노드 가져오기
        root = tree.getroot()

        # opf:metadata 태그 찾기
        metadata_node = root.find("opf:metadata", cls.NS)
        # 만약 <opf:metadata> 태그가 없으면 그냥 빈 Metadata 객체를 반환
        if metadata_node is None :
            return metadata

        # 제목 추출
        metadata.title = cls.get_title(metadata_node)
        
        # <opf:metadata> 안에 있는 모든 <opf:meta> 태그를 찾는 코드
        for meta_node in metadata_node.findall("opf:meta", cls.NS) :
            # 각 <opf:meta> 태그의 name 속성 추출
            meta_name = meta_node.attrib.get("name")
            # META_MAP에 등록된 항목만 처리
            if meta_name not in cls.META_MAP : 
                continue

            # Metadata 객체에 값 저장
            setattr(
                metadata,
                cls.META_MAP[meta_name],
                meta_node.text
            )

        return metadata

    @classmethod
    def get_title(cls, metadata_node : Any):
        """
        <opf:metadata> 안에 있는 <opf:title> 태그를 찾아서 제목을 반환
        """

        # <opf:title> 태그를 찾음
        title_node = metadata_node.find("opf:title", cls.NS)
        # 제목 태그가 없으면 None 반환.
        if title_node is None : 
            return None

        return title_node.text
