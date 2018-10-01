# -*- coding: utf-8 -*-

"""Testing constants for Bio2BEL MeSH."""

import os

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_mesh import Manager

__all__ = [
    'TemporaryCacheClass',
]

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_MESH_DESCRIPTORS_PATH = os.path.join(HERE, 'test_mesh_descriptors.xml')


class TemporaryCacheClass(AbstractTemporaryCacheClassMixin):
    """A test case containing a temporary database and a Bio2BEL MeSH manager."""

    Manager = Manager
    manager: Manager

    @classmethod
    def populate(cls):
        """Populate the database with test data."""
        cls.manager.populate(path=TEST_MESH_DESCRIPTORS_PATH)
