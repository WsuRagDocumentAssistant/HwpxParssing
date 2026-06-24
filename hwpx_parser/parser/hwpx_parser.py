#================================================
# hwpx_parser.py
#================================================

# 아직 정의 중인 클래스 이름도 타입 힌트에 편하게 쓸 수 있게 해주는 것
from __future__ import annotations

# 파일 경로를 문자열이 아니라 객체처럼 다루기 위한 것
from pathlib import Path
# .hwpx 또는 .zip 파일을 압축 파일처럼 열기 위한 것, HWPX 파일은 내부적으로 ZIP 구조이기 때문
import zipfile

"""
BaseBlock
→ 문단, 표, 이미지 블록의 공통 부모 객체

Metadata
→ 문서 메타데이터 저장 객체

MetadataParser
→ content.hpf에서 메타데이터 추출하는 파서

SectionParser
→ section0.xml, section1.xml 같은 본문 XML을 파싱하는 파서
"""

#------------------------------------------------

class HwpxParser:
    """
    한글 문서 자동 파싱
    """

    def __init__(self, doc_save_path: str, source: str):
        """
        doc_save_path : 파싱될 문서가 저장될 위치
        source : 파싱할 문서 위치
        """
        
        # source 문자열을 Path 객체로 변환하여 self.__doc에 저장
        self.__doc = Path(source)
        # 파일 이름을 추출하여 self.filename에 저장 (확장자 제외)
        self.filename = self.__doc.stem

        # 압축 해제 결과를 저장할 기준 폴더 설정
        self.__DOC_SAVE_PATH = Path(doc_save_path)
        # 압축을 실제로 풀 위치
        self.__UNPACKED_DIR_PATH = self.__DOC_SAVE_PATH / "unpacked" / self.filename
        # 이미지 파일이 저장된 폴더 경로
        self.__IMGS_DIR_PATH = self.__UNPACKED_DIR_PATH / "BinData"
        # 압축 해제된 폴더 내에서 본문 XML, 메타데이터, header.xml 파일이 위치한 폴더 경로
        self.__CONTENTS_DIR_PATH = self.__UNPACKED_DIR_PATH / "Contents"
        # 메타데이터 파일 경로
        self.__METADATA_FILE_PATH = self.__CONTENTS_DIR_PATH / "content.hpf"
        # header.xml 파일 경로
        self.__HEADER_FILE_PATH = self.__CONTENTS_DIR_PATH / "header.xml"

        # 압축 해제
        self.__ensure_unpacked()

        # Contents 폴더 안에서 section*.xml 파일을 전부 찾는 코드, 숫자 기준으로 정렬
        self.__SECTION_FILE_PATHS = sorted(
            self.__CONTENTS_DIR_PATH.glob("section*.xml"),
            key=self.__section_sort_key,
        )

        # 메타데이터를 파싱해서 self.metadata에 저장
        self.metadata: Metadata = self.__create_metadata()
        # section*.xml을 파싱해서 self.section_data에 저장
        #self.section_data: list[BaseBlock] = self.__create_sectiondata()

    def __ensure_unpacked(self) -> None:
        """
        압축 해제 여부 확인 및 필요 시 압축 해제
        """
        # 압축 해제 여부 확인
        if self.__METADATA_FILE_PATH.exists() and list(self.__CONTENTS_DIR_PATH.glob("section*.xml")):
            return

        # 압축 해제
        self.__unpackzing_hwpx()

    def __unpackzing_hwpx(self) -> None:
        """
        HWPX 파일 압축 해제
        """

        # 압축을 풀 폴더 생성
        self.__UNPACKED_DIR_PATH.mkdir(parents=True, exist_ok=True)

        # 압축 해제
        with zipfile.ZipFile(self.__doc, "r") as zip_ref:
            zip_ref.extractall(self.__UNPACKED_DIR_PATH)

    def __create_metadata(self) -> Metadata:
        """
        content.hpf에서 메타데이터 추출
        """
        return MetadataParser.parse(str(self.__METADATA_FILE_PATH))

    # def __create_sectiondata(self) -> list[BaseBlock]:
    #     """
    #     section*.xml에서 본문 데이터 추출
    #     """

    #     """
    #     1. section XML 파일 목록
    #     2. header.xml 경로
    #     3. BinData 이미지 폴더 경로
    #     """
    #     return SectionParser.parse(
    #         [str(path) for path in self.__SECTION_FILE_PATHS],
    #         header_source=str(self.__HEADER_FILE_PATH),
    #         image_dir_path=str(self.__IMGS_DIR_PATH),
    #     )

    def file_info(self) -> None:
        """
        파일 정보 출력
        """
        print("===========================================")
        print(f"source: {self.__doc}")
        print(f"filename: {self.filename}")
        print(f"sections: {len(self.section_data)}")
        print(f"title: {self.metadata.title}")
        print(f"creator: {self.metadata.creator}")
        print("===========================================")

    @classmethod
    def __section_sort_key(cls, source: Path) -> tuple[int, str]:
        """
        section*.xml 파일을 숫자 기준으로 정렬하기 위한 키 생성
        """

        # 파일명에서 확장자를 뺀 이름
        stem = source.stem

        # 파일명에서 숫자만 추출
        suffix = "".join(ch for ch in stem if ch.isdigit())

        if not suffix:
            return (10**9, stem)

        return (int(suffix), stem)