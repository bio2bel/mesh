# -*- coding: utf-8 -*-

"""Parser for the MeSH descriptors."""

import json
import logging
import os

from tqdm import tqdm

from bio2bel import make_downloader
from .utils import get_concepts, parse_xml
from ..constants import DESCRIPTOR_JSON_PATH, DESCRIPTOR_PATH, DESCRIPTOR_URL

__all__ = [
    'download_descriptors',
    'get_descriptors_root',
    'get_descriptors',
]

log = logging.getLogger(__name__)

download_descriptors = make_downloader(DESCRIPTOR_URL, DESCRIPTOR_PATH)


def get_descriptors_root(path=None, cache=True, force_download=False):
    # Parse xml file as an ElementTree

    if path is None and cache:
        path = download_descriptors(force_download=force_download)

    return parse_xml(path)


def _get_descriptor_qualifiers(descriptor):
    rv = []

    for qualifier in descriptor.findall('AllowableQualifiersList/AllowableQualifier/QualifierReferredTo'):
        qualifier_entry = {
            'qualifier_ui': qualifier.findtext('QualifierUI'),
            'name': qualifier.findtext('QualifierName/String'),
        }
        rv.append(qualifier_entry)

    return rv


def _get_descriptor(e):
    descriptor_entry = {
        'descriptor_ui': e.findtext('DescriptorUI'),
        'name': e.findtext('DescriptorName/String'),
        'tree_numbers': list({
            x.text
            for x in e.findall('TreeNumberList/TreeNumber')
        }),
        'concepts': get_concepts(e),
        # TODO handle AllowableQualifiersList
    }

    return descriptor_entry


def _get_descriptors(root):
    log.info('extract MeSH descriptors, concepts, and terms')

    rv = [
        _get_descriptor(descriptor)
        for descriptor in tqdm(root, desc='Descriptors')
    ]

    # cache tree numbers
    tree_number_to_descriptor_ui = {
        tree_number: descriptor['descriptor_ui']
        for descriptor in rv
        for tree_number in descriptor['tree_numbers']
    }

    # add in parents to each descriptor based on their tree numbers
    for descriptor in rv:
        parents_descriptor_uis = set()
        for tree_number in descriptor['tree_numbers']:
            try:
                parent_tn, self_tn = tree_number.rsplit('.', 1)
                parent_descriptor_ui = tree_number_to_descriptor_ui[parent_tn]
                parents_descriptor_uis.add(parent_descriptor_ui)
            except ValueError:
                pass
        descriptor['parents'] = list(parents_descriptor_uis)
    return rv


def get_descriptors(path=None, cache=True, force_download=False):
    if os.path.exists(DESCRIPTOR_JSON_PATH):
        log.info('loading cached descriptors json')
        with open(DESCRIPTOR_JSON_PATH) as file:
            return json.load(file)

    root = get_descriptors_root(path=path, cache=cache, force_download=force_download)
    rv = _get_descriptors(root)

    with open(DESCRIPTOR_JSON_PATH, 'w') as file:
        log.info('caching descriptors json')
        json.dump(rv, file, indent=2)

    return rv
