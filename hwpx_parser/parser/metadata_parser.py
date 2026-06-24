#================================================
# metadata_parser.py
#================================================

from __future__ import annotations

from ..blocks.meta_data import Metadata
from .base_parser import BaseParser

from typing_extensions import override
import xml.etree.ElementTree as ET
from typing import Any

#------------------------------------------------

class MetadataParser(BaseParser):

    NS : dict[str,str] = { 
        "opf" : "http://www.idpf.org/2007/opf/" 
    }
    
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
        metadata = Metadata()

        tree = ET.parse(metadata_source)
        root = tree.getroot()

        metadata_node = root.find("opf:metadata", cls.NS)
        if metadata_node is None :
            return metadata

        metadata.title = cls.get_title(metadata_node)
        
        for meta_node in metadata_node.findall("opf:meta", cls.NS) :
            meta_name = meta_node.attrib.get("name")
            if meta_name not in cls.META_MAP : 
                continue

            setattr(
                metadata,
                cls.META_MAP[meta_name],
                meta_node.text
            )

        return metadata

    @classmethod
    def get_title(cls, metadata_node : Any):
        title_node = metadata_node.find("opf:title", cls.NS)
        if title_node is None : 
            return None

        return title_node.text
