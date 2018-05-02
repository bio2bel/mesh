# -*- coding: utf-8 -*-

"""Parser for the MeSH descriptors."""

import logging

from tqdm import tqdm

from bio2bel import make_downloader
from .utils import parse_xml
from ..constants import DESCRIPTOR_PATH, DESCRIPTOR_URL

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


def _get_descriptors(root):
    log.info('extract mesh terms')
    term_dicts = list()

    for descriptor in tqdm(root, desc='Descriptors'):
        for concept in descriptor.findall('ConceptList/Concept'):
            for term in concept.findall('TermList/Term'):
                term_dict = {
                    'DescriptorUI': descriptor.findtext('DescriptorUI'),
                    'ConceptUI': concept.findtext('ConceptUI'),
                    'TermUI': term.findtext('TermUI'),
                    'TermName': term.findtext('String')
                }
                term_dict.update(concept.attrib)
                term_dict.update(term.attrib)
                term_dicts.append(term_dict)

    return term_dicts


def _get_terms(root):
    log.info('parse mesh xml release')

    terms = [
        {
            'mesh_id': elem.findtext('DescriptorUI'),
            'mesh_name': elem.findtext('DescriptorName/String'),
            'semantic_types': list({
                x.text
                for x in elem.findall('ConceptList/Concept/SemanticTypeList/SemanticType/SemanticTypeUI')
            }),
            'tree_numbers': [
                x.text
                for x in elem.findall('TreeNumberList/TreeNumber')
            ]
        }
        for elem in tqdm(root, desc='Terms')
    ]

    # Determine ontology parents
    tree_number_to_id = {
        tn: term['mesh_id']
        for term in terms for tn in term['tree_numbers']
    }

    for term in terms:
        parents = set()
        for tree_number in term['tree_numbers']:
            try:
                parent_tn, self_tn = tree_number.rsplit('.', 1)
                parents.add(tree_number_to_id[parent_tn])
            except ValueError:
                pass
        term['parents'] = list(parents)

    return terms


def get_descriptors(path=None, cache=True, force_download=False):
    root = get_descriptors_root(path=path, cache=cache, force_download=force_download)

    d = _get_descriptors(root)
    t = _get_terms(root)
