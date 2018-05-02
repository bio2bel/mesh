# -*- coding: utf-8 -*-

import os

from bio2bel import get_data_dir

MODULE_NAME = 'mesh'
DATA_DIR = get_data_dir(MODULE_NAME)

DESCRIPTOR_URL = 'ftp://nlmpubs.nlm.nih.gov/online/mesh/.xmlmesh/desc2017.gz'
DESCRIPTOR_PATH = os.path.join(DATA_DIR, 'desc2017.gz')
DESCRIPTOR_JSON_PATH = os.path.join(DATA_DIR, 'desc2017.json')

SUPPLEMENT_URL = 'ftp://nlmpubs.nlm.nih.gov/online/mesh/.xmlmesh/supp2017.gz'
SUPPLEMENT_PATH = os.path.join(DATA_DIR, 'supp2017.gz')
SUPPLEMENT_JSON_PATH = os.path.join(DATA_DIR, 'supp2017.json')
