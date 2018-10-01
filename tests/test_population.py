# -*- coding: utf-8 -*-

"""Testing constants for Bio2BEL MeSH."""

from tests.constants import TemporaryCacheClass


class TestPopulation(TemporaryCacheClass):
    """Tests for population of the database."""

    def test_counts(self):
        """Test the right number of things are added."""
        self.assertEqual(6, self.manager.count_descriptors())
