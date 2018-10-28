# -*- coding: utf-8 -*-

"""Testing constants for Bio2BEL MeSH."""

import os

__all__ = [
    'TEST_DESCRIPTORS_PATH',
    'TEST_SUPPLEMENT_PATH',
]

HERE = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIRECTORY = os.path.join(HERE, 'resources')
TEST_DESCRIPTORS_PATH = os.path.join(RESOURCES_DIRECTORY, 'test.desc2017.xml.gz')
TEST_SUPPLEMENT_PATH = os.path.join(RESOURCES_DIRECTORY, 'test.supp2017.xml.gz')
