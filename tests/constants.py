# -*- coding: utf-8 -*-

"""Testing constants for Bio2BEL MeSH."""

import os

__all__ = [
    'TEST_DESCRIPTORS_PATH',
    'TEST_SUPPLEMENT_PATH',
]

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_DESCRIPTORS_PATH = os.path.join(HERE, 'test.desc2017.xml')
TEST_SUPPLEMENT_PATH = os.path.join(HERE, 'test.supp2017.xml')
