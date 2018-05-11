# -*- coding: utf-8 -*-

"""SQLAlchemy database models."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from .constants import MODULE_NAME

Base = declarative_base()

DESCRIPTOR_TABLE_NAME = f'{MODULE_NAME}_descriptor'
CONCEPT_TABLE_NAME = f'{MODULE_NAME}_concept'
TERM_TABLE_NAME = f'{MODULE_NAME}_term'
TREE_TABLE_NAME = f'{MODULE_NAME}_tree'


class Descriptor(Base):
    __tablename__ = DESCRIPTOR_TABLE_NAME

    id = Column(Integer, primary_key=True)

    descriptor_ui = Column(String(255), nullable=False, unique=True, index=True,
                           doc='MeSH descriptor identifier. Starts with D.')

    name = Column(String(255), nullable=False, unique=True, index=True, doc='MeSH descriptor label')

    def __str__(self):
        return self.name


class Concept(Base):
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


class Tree(Base):
    __tablename__ = TREE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False, unique=True, index=True, doc='MeSH tree number')

    descriptor_id = Column(Integer, ForeignKey(f'{DESCRIPTOR_TABLE_NAME}.id'), nullable=False)
    descriptor = relationship(Descriptor, backref=backref('trees'))

    def __str__(self):
        return self.name
