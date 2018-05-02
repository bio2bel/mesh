# -*- coding: utf-8 -*-

"""Bio2BEL MeSH manager."""

import logging
import time
from typing import List, Mapping, Optional

from tqdm import tqdm

from bio2bel import AbstractManager
from .constants import MODULE_NAME
from .models import Base, Concept, Descriptor, Term, Tree
from .parsers import get_descriptors

__all__ = [
    'Manager',
]

log = logging.getLogger(__name__)


class Manager(AbstractManager):
    """Bio2BEL MeSH manager."""

    module_name = MODULE_NAME
    flask_admin_models = [Descriptor, Concept, Term, Tree]

    @property
    def _base(self):
        return Base

    def is_populated(self) -> bool:
        """Check if the database is already populated."""
        raise 0 < self.count_terms()

    def count_descriptors(self) -> int:
        """Count the number of descriptors in the database."""
        return self._count_model(Descriptor)

    def list_descriptors(self) -> List[Descriptor]:
        """List the descriptors from the database."""
        return self._list_model(Descriptor)

    def get_descriptor_by_ui(self, ui) -> Optional[Descriptor]:
        return self.session.query(Descriptor.descriptor_ui == ui).one_or_none()

    def count_concepts(self) -> int:
        """Count the number of concepts in the database."""
        return self._count_model(Concept)

    def list_concepts(self) -> List[Concept]:
        """List the concepts from the database."""
        return self._list_model(Concept)

    def get_concept_by_ui(self, ui) -> Optional[Concept]:
        return self.session.query(Concept.concept_ui == ui).one_or_none()

    def count_terms(self) -> int:
        """Count the number of terms in the database."""
        return self._count_model(Term)

    def list_terms(self) -> List[Term]:
        """List the terms from the database."""
        return self._list_model(Term)

    def get_term_by_ui(self, ui) -> Optional[Term]:
        return self.session.query(Term.term_ui == ui).one_or_none()

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(
            terms=self.count_terms(),
            concepts=self.count_concepts(),
            descriptors=self.count_descriptors()
        )

    def _populate_descriptors(self):
        log.info('loading database')
        ui_descriptor = {d.descriptor_ui: d for d in self.list_descriptors()}
        ui_concept = {d.concept_ui: d for d in self.list_concepts()}
        ui_term = {d.term_ui: d for d in self.list_terms()}

        log.info('getting descriptor xml')
        descriptors = get_descriptors()

        log.info('building models')
        for descriptor_xml in tqdm(descriptors):
            descriptor_ui = descriptor_xml['descriptor_ui']

            descriptor = ui_descriptor.get(descriptor_ui)
            if descriptor is None:
                descriptor = Descriptor(
                    descriptor_ui=descriptor_ui,
                    name=descriptor_xml['name'],
                    trees=[
                        Tree(name=name)
                        for name in descriptor_xml['tree_numbers']
                    ],
                )
                self.session.add(descriptor)

            for concept_xml in descriptor_xml['concepts']:
                concept_ui, concept_name = concept_xml['concept_ui'], concept_xml['name']

                concept = ui_concept.get(concept_ui)
                if concept is None:
                    concept = Concept(concept_ui=concept_ui, name=concept_name, descriptor=descriptor)
                    self.session.add(concept)

                for term_xml in concept_xml['terms']:

                    # if term_xml['IsPermutedTermYN'] == 'Y':
                    #    continue  # FIXME need better solution for these

                    term_ui, term_name = term_xml['term_ui'], term_xml['name']

                    term = ui_term.get(term_ui)
                    if term is None:
                        term = Term(term_ui=term_ui, name=term_name, concept=concept)
                        self.session.add(term)

        t = time.time()
        log.info('committing models')
        self.session.commit()
        log.info('committed models in %.2f seconds', time.time() - t)

    def populate(self):
        self._populate_descriptors()

    @classmethod
    def get_cli(cls):
        main = super().get_cli()
        import click
        import json
        @main.command()
        @click.option('-o', '--output', type=click.File('w'))
        def download(output):
            """Download and mock-parse everything"""
            descriptors = get_descriptors()
            json.dump(descriptors, output, indent=2)

        return main
