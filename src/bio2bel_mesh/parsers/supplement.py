# -*- coding: utf-8 -*-

"""Parser for the MeSH supplemental."""

import json
import logging
import os
from typing import List, Mapping, Optional
from xml.etree.ElementTree import Element

from tqdm import tqdm

from bio2bel import make_downloader
from .utils import get_concepts, parse_xml
from ..constants import SUPPLEMENT_JSON_PATH, SUPPLEMENT_PATH, SUPPLEMENT_URL

__all__ = [
    'download_supplement',
    'get_supplement_root',
    'get_supplementary_records',
]

log = logging.getLogger(__name__)

download_supplement = make_downloader(SUPPLEMENT_URL, SUPPLEMENT_PATH)


def get_supplementary_records(path: Optional[str] = None, cache: bool = True, force_download: bool = False) -> List[
    Mapping]:  # noqa: E126
    """Get supplementary records."""
    if path is None and os.path.exists(SUPPLEMENT_JSON_PATH):
        log.info('loading cached supplemental records json')
        with open(SUPPLEMENT_JSON_PATH) as file:
            return json.load(file)

    root = get_supplement_root(path=path, cache=cache, force_download=force_download)
    rv = _get_terms(root)

    if path is None:
        with open(SUPPLEMENT_JSON_PATH, 'w') as file:
            log.info('caching supplemental records json')
            json.dump(rv, file, indent=2)

    return rv


def get_supplement_root(path: Optional[str] = None, cache: bool = True, force_download: bool = False) -> Element:
    """Parse xml file as an ElementTree."""
    if path is None and cache:
        path = download_supplement(force_download=force_download)
    return parse_xml(path)


def _get_terms(element: Element) -> List[Mapping]:
    return [
        {
            # this basically takes the same form as a descriptor
            'descriptor_ui': record.findtext('SupplementalRecordUI'),
            'name': record.findtext('SupplementalRecordName/String'),
            'scr': record.get('SCRClass'),
            'concepts': get_concepts(record),
        }
        for record in tqdm(element.findall('SupplementalRecord'), desc='Supplemental Records')
    ]
