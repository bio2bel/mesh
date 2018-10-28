# -*- coding: utf-8 -*-

"""SQLAlchemy database models for Bio2BEL MeSH."""

import itertools as itt
from typing import Mapping, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import backref, relationship

from .constants import MODULE_NAME

Base: DeclarativeMeta = declarative_base()

DESCRIPTOR_TABLE_NAME = f'{MODULE_NAME}_descriptor'
CONCEPT_TABLE_NAME = f'{MODULE_NAME}_concept'
TERM_TABLE_NAME = f'{MODULE_NAME}_term'
TREE_TABLE_NAME = f'{MODULE_NAME}_tree'


class Descriptor(Base):
    """MeSH Descriptor."""

    __tablename__ = DESCRIPTOR_TABLE_NAME

    id = Column(Integer, primary_key=True)

    descriptor_ui = Column(String(255), nullable=False, unique=True, index=True,
                           doc='MeSH descriptor identifier. Starts with D.')

    name = Column(String(255), nullable=False, unique=True, index=True, doc='MeSH descriptor label')

    def __str__(self):
        return self.name

    @property
    def is_pathology(self) -> bool:
        """Check if this term is a pathology/phenotype."""
        return self._has_tree_prefixes(['C', 'F'])

    @property
    def is_process(self) -> bool:
        """Check if this term is a process."""
        return self._has_tree_prefix('G') and self._not_has_tree_prefixes(['G01', 'G15', 'G17'])

    @property
    def is_chemical(self) -> bool:
        """Check if this term is a chemical."""
        return self._has_tree_prefix('D')

    @property
    def bel_encoding(self) -> Optional[str]:
        """Get the BEL encoding for this descriptor."""
        if self.is_pathology:
            return 'O'
        if self.is_process:
            return 'B'
        if self.is_chemical:
            return 'A'

    def _not_has_tree_prefixes(self, prefixes) -> bool:
        return all(
            prefix not in tree.name
            for prefix, tree in itt.product(prefixes, self.trees)
        )

    def _has_tree_prefixes(self, prefixes) -> bool:
        """Check if any of the tree entries have any of the given prefixes."""
        return any(
            prefix in tree.name
            for prefix, tree in itt.product(prefixes, self.trees)
        )

    def _has_tree_prefix(self, prefix: str) -> bool:
        """Check if any of the tree entries for this descriptor have the given prefix."""
        return any(
            prefix in tree.name
            for tree in self.trees
        )


class Concept(Base):
    """MeSH Concept."""

    __tablename__ = CONCEPT_TABLE_NAME

    id = Column(Integer, primary_key=True)

    concept_ui = Column(String(255), nullable=False, unique=True, index=True,
                        doc='MeSH concept identifier. Starts with M.')
    name = Column(String(255), nullable=False, unique=True, index=True, doc='MeSH concept label')

    descriptor_id = Column(Integer, ForeignKey(f'{DESCRIPTOR_TABLE_NAME}.id'), nullable=False)
    descriptor = relationship(Descriptor)

    def __str__(self):
        return self.name


class Term(Base):
    """MeSH Term."""

    __tablename__ = TERM_TABLE_NAME

    id = Column(Integer, primary_key=True)

    term_ui = Column(String(255), nullable=False, index=True,
                     doc='MeSH concept identifier. Starts with T. Might be duplicate for permutations')
    name = Column(String(255), nullable=False, index=True, doc='MeSH term label')

    concept_id = Column(Integer, ForeignKey(f'{CONCEPT_TABLE_NAME}.id'), nullable=False)
    concept = relationship(Concept)

    # ConceptPreferredTermYN = Column(Boolean)
    # IsPermutedTermYN = Column(Boolean)
    # LexicalTag = "TRD"
    # RecordPreferredTermYN = Column(Boolean)

    def __str__(self):
        return self.name

    def to_json(self) -> Mapping:
        """Return this term as a JSON object."""
        return {
            'descriptor_ui': self.concept.descriptor.descriptor_ui,
            'descriptor_name': self.concept.descriptor.name,
            'concept_ui': self.concept.concept_ui,
            'concept_name': self.concept.name,
            'term_ui': self.term_ui,
            'term_name': self.name
        }


class Tree(Base):
    """MeSH Tree."""

    __tablename__ = TREE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False, unique=True, index=True, doc='MeSH tree number')

    descriptor_id = Column(Integer, ForeignKey(f'{DESCRIPTOR_TABLE_NAME}.id'), nullable=False)
    descriptor = relationship(Descriptor, backref=backref('trees'))

    def __str__(self):
        return self.name
