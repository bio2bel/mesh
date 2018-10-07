# -*- coding: utf-8 -*-

"""Parser utilities."""

import gzip
import logging
import time
import xml.etree.ElementTree as ET
from typing import List, Mapping
from xml.etree.ElementTree import Element


log = logging.getLogger(__name__)


def parse_xml(path: str) -> Element:
    """Parse an XML file from a path to a GZIP file."""
    t = time.time()
    log.info('parsing xml from %s', path)
    with gzip.open(path) as xml_file:
        tree = ET.parse(xml_file)
    log.info('parsed xml in %.2f seconds', time.time() - t)

    return tree.getroot()


def get_terms(element: Element) -> List[Mapping]:
    """Get all of the terms for a concept."""
    return [
        {
            'term_ui': term.findtext('TermUI'),
            'name': term.findtext('String'),
            **term.attrib
        }
        for term in element.findall('TermList/Term')
    ]


def get_concepts(element: Element) -> List[Mapping]:
    """Get concepts from a record."""
    return [
        {
            'concept_ui': concept.findtext('ConceptUI'),
            'name': concept.findtext('ConceptName/String'),
            'semantic_types': list({
                x.text
                for x in concept.findall('SemanticTypeList/SemanticType/SemanticTypeUI')
            }),
            'terms': get_terms(concept),
            # TODO handle ConceptRelationList
            **concept.attrib
        }
        for concept in element.findall('ConceptList/Concept')
    ]
