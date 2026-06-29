#================================================
# test.py
#================================================

from hwpx_parser.parser.hwpx_parser import HwpxParser 
from hwpx_parser.model.hwpx_model import HwpxModel

import hwpx_parser

#────────────────────────────────────────────────

if __name__ == "__main__":
    parser = HwpxParser(
        "doc/2주기(2023년) 2022 ~ 2024 대학혁신지원사업 성과평가보고서.hwpx",
        "doc/"
    )
    model : HwpxModel = parser.parse()
    model.print()