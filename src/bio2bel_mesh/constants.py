# -*- coding: utf-8 -*-

"""Constants for Bio2BEL MeSH."""

import os

from bio2bel import get_data_dir

VERSION = '0.2.0'

MODULE_NAME = 'mesh'
DATA_DIR = get_data_dir(MODULE_NAME)

YEAR = '2017'

DESCRIPTOR_URL = f'ftp://nlmpubs.nlm.nih.gov/online/mesh/.xmlmesh/desc{YEAR}.gz'
DESCRIPTOR_PATH = os.path.join(DATA_DIR, f'desc{YEAR}.gz')
DESCRIPTOR_JSON_PATH = os.path.join(DATA_DIR, f'desc{YEAR}.json')

SUPPLEMENT_URL = f'ftp://nlmpubs.nlm.nih.gov/online/mesh/.xmlmesh/supp{YEAR}.gz'
SUPPLEMENT_PATH = os.path.join(DATA_DIR, f'supp{YEAR}.gz')
SUPPLEMENT_JSON_PATH = os.path.join(DATA_DIR, f'supp{YEAR}.json')
