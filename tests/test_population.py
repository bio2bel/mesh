# -*- coding: utf-8 -*-

"""Tests for Bio2BEL MeSH."""

from tests.cases import TemporaryCacheClass


class TestPopulation(TemporaryCacheClass):
    """Tests for population of the database."""

    def test_counts(self):
        """Test the right number of things are added."""
        self.assertEqual(11, self.manager.count_descriptors())
