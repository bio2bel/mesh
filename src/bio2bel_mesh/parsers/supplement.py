# -*- coding: utf-8 -*-

"""Parser for the MeSH supplemental."""

import logging

from tqdm import tqdm

from bio2bel import make_downloader
from .utils import parse_xml
from ..constants import SUPPLEMENT_PATH, SUPPLEMENT_URL

__all__ = [
    'download_supplement',
    'get_supplement_root',
    'get_supplement',
]

log = logging.getLogger(__name__)

download_supplement = make_downloader(SUPPLEMENT_URL, SUPPLEMENT_PATH)


def get_supplement_root(path=None, cache=True, force_download=False):
    # Parse xml file as an ElementTree
    if path is None and cache:
        path = download_supplement(force_download=force_download)

    return parse_xml(path)


def _get_records(root):
    record_dicts = list()

    for record in tqdm(root, desc='Supplementary Entries'):
        record_dict = dict()
        record_dict['SCRClass'] = record.get('SCRClass')
        record_dict['SupplementalRecordUI'] = record.findtext('SupplementalRecordUI')
        record_dict['SupplementalRecordName'] = record.findtext('SupplementalRecordName/String')
        record_dicts.append(record_dict)

    return record_dicts


def _get_terms(root):
    term_dicts = list()
    for record in tqdm(root.findall('SupplementalRecord'), desc='Supplemental Records'):
        for concept in record.findall('ConceptList/Concept'):
            for term in concept.findall('TermList/Term'):
                term_dict = {
                    'SupplementalRecordUI': record.findtext('SupplementalRecordUI'),
                    'ConceptUI': concept.findtext('ConceptUI'),
                    'TermUI': term.findtext('TermUI'),
                    'TermName': term.findtext('String')
                }
                term_dict.update(concept.attrib)
                term_dict.update(term.attrib)
                term_dicts.append(term_dict)

    return term_dicts


def get_supplement(path=None, cache=True, force_download=False):
    root = get_supplement_root(path=path, cache=cache, force_download=force_download)

    r = _get_records(root)
    t = _get_terms(root)
