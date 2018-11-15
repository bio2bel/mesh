# -*- coding: utf-8 -*-

"""Parser for the MeSH descriptors."""

import json
import logging
import os
from typing import Dict, List, Mapping, Optional
from xml.etree.ElementTree import Element

from tqdm import tqdm

from bio2bel import make_downloader
from .utils import get_concepts, parse_xml
from ..constants import DESCRIPTOR_JSON_PATH, DESCRIPTOR_PATH, DESCRIPTOR_URL

__all__ = [
    'download_descriptors',
    'get_descriptors_root',
    'get_descriptor_records',
]

log = logging.getLogger(__name__)

download_descriptors = make_downloader(DESCRIPTOR_URL, DESCRIPTOR_PATH)


def get_descriptor_records(path: Optional[str] = None, cache=True, force_download=False) -> List[Mapping]:
    """Get descriptors from a path."""
    if path is None and os.path.exists(DESCRIPTOR_JSON_PATH):
        log.info(f'loading cached descriptors json from {DESCRIPTOR_JSON_PATH}')
        with open(DESCRIPTOR_JSON_PATH) as file:
            return json.load(file)

    root = get_descriptors_root(path=path, cache=cache, force_download=force_download)
    rv = _get_descriptors(root)

    if path is None:
        with open(DESCRIPTOR_JSON_PATH, 'w') as file:
            log.info('caching descriptors json')
            json.dump(rv, file, indent=2)

    return rv


def get_descriptors_root(path: Optional[str] = None, cache: bool = True, force_download: bool = False) -> Element:
    """Parse xml file as an ElementTree."""
    if path is None and cache:
        path = download_descriptors(force_download=force_download)

    return parse_xml(path)


def _get_descriptors(element: Element) -> List[Mapping]:
    log.info('extract MeSH descriptors, concepts, and terms')

    rv = [
        _get_descriptor(descriptor)
        for descriptor in tqdm(element, desc='Descriptors')
    ]
    log.debug(f'got {len(rv)} descriptors')

    # cache tree numbers
    tree_number_to_descriptor_ui = {
        tree_number: descriptor['descriptor_ui']
        for descriptor in rv
        for tree_number in descriptor['tree_numbers']
    }
    log.debug(f'got {len(tree_number_to_descriptor_ui)} tree mappings')

    # add in parents to each descriptor based on their tree numbers
    for descriptor in rv:
        parents_descriptor_uis = set()
        for tree_number in descriptor['tree_numbers']:
            parent_tn, self_tn = tree_number.rsplit('.', 1)

            parent_descriptor_ui = tree_number_to_descriptor_ui.get(parent_tn)
            if parent_descriptor_ui is not None:
                parents_descriptor_uis.add(parent_descriptor_ui)
            else:
                log.debug('missing tree number: %s', parent_tn)

        descriptor['parents'] = list(parents_descriptor_uis)

    return rv


def _get_descriptor(element: Element) -> Dict:
    return {
        'descriptor_ui': element.findtext('DescriptorUI'),
        'name': element.findtext('DescriptorName/String'),
        'tree_numbers': list({
            x.text
            for x in element.findall('TreeNumberList/TreeNumber')
        }),
        'concepts': get_concepts(element),
        # TODO handle AllowableQualifiersList
        # TODO add ScopeNote as description
    }


def _get_descriptor_qualifiers(descriptor: Element) -> List[Mapping]:
    return [
        {
            'qualifier_ui': qualifier.findtext('QualifierUI'),
            'name': qualifier.findtext('QualifierName/String'),
        }
        for qualifier in descriptor.findall('AllowableQualifiersList/AllowableQualifier/QualifierReferredTo')
    ]
