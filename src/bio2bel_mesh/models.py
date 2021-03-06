# -*- coding: utf-8 -*-

"""SQLAlchemy database models for Bio2BEL MeSH."""

import itertools as itt
from typing import Mapping, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import backref, relationship

import pybel.dsl
from pybel.constants import belns_encodings
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

    is_anatomy = Column(Boolean, default=False)
    is_organism = Column(Boolean, default=False)
    is_pathology = Column(Boolean, default=False)
    is_chemical = Column(Boolean, default=False)
    is_protein = Column(Boolean, default=False)
    is_complex = Column(Boolean, default=False)
    is_measurement = Column(Boolean, default=False)
    is_process = Column(Boolean, default=False)

    def __str__(self):
        return self.name

    @property
    def bel_encoding(self) -> str:
        """Get the BEL encoding for this descriptor."""
        rv = set()

        if self.is_anatomy or self.is_chemical or self.is_organism:
            rv.add('A')
        if self.is_pathology or self.is_measurement:
            rv.add('O')
        if self.is_process:
            rv.add('B')
        if self.is_protein:
            rv.update('GRP')
        if self.is_complex:
            rv.add('C')

        if not rv:
            rv = set(belns_encodings)

        return ''.join(sorted(rv))

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

    def to_bel(self) -> Optional[pybel.dsl.BaseEntity]:
        """Convert this MeSH term to a PyBEL DSL entry."""
        if self.is_pathology:
            dsl = pybel.dsl.Pathology
        elif self.is_process:
            dsl = pybel.dsl.BiologicalProcess
        elif self.is_chemical:
            dsl = pybel.dsl.Abundance
        else:
            def dsl(**kwargs) -> None:
                """Return none."""

        return dsl(
            namespace='mesh',
            name=self.name,
            identifier=self.descriptor_ui,
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
