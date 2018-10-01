# -*- coding: utf-8 -*-

import gzip
import logging
import time
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)


def parse_xml(path):
    t = time.time()
    log.info('parsing xml from %s', path)
    with gzip.open(path) as xml_file:
        tree = ET.parse(xml_file)
    log.info('parsed xml in %.2f seconds', time.time() - t)

    return tree.getroot()


def get_terms(e):
    """Get all of the terms for a concept."""
    rv = []

    for term in e.findall('TermList/Term'):
        term_entry = {
            'term_ui': term.findtext('TermUI'),
            'name': term.findtext('String')
        }
        term_entry.update(term.attrib)
        rv.append(term_entry)

    return rv


def get_concept_relations(concept):
    raise NotImplementedError


def get_concepts(e):
    rv = []

    for concept in e.findall('ConceptList/Concept'):
        concept_entry = {
            'concept_ui': concept.findtext('ConceptUI'),
            'name': concept.findtext('ConceptName/String'),
            'semantic_types': list({
                x.text
                for x in concept.findall('SemanticTypeList/SemanticType/SemanticTypeUI')
            }),
            'terms': get_terms(concept),
            # TODO handle ConceptRelationList
        }
        concept_entry.update(concept.attrib)
        rv.append(concept_entry)

    return rv
