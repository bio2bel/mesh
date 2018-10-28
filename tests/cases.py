# -*- coding: utf-8 -*-

"""Test cases for Bio2BEL MeSH."""

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_mesh import Manager
from tests.constants import TEST_DESCRIPTORS_PATH, TEST_SUPPLEMENT_PATH


class TemporaryCacheClass(AbstractTemporaryCacheClassMixin):
    """A test case containing a temporary database and a Bio2BEL MeSH manager."""

    Manager = Manager
    manager: Manager

    @classmethod
    def populate(cls):
        """Populate the database with test data."""
        cls.manager.populate(
            descriptors_path=TEST_DESCRIPTORS_PATH,
            supplement_path=TEST_SUPPLEMENT_PATH,
        )
