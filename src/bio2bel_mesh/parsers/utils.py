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
