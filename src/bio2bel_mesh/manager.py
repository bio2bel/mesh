# -*- coding: utf-8 -*-

"""Bio2BEL MeSH manager."""

import logging
from collections import Counter
from typing import Iterable, List, Mapping, Optional, Tuple

import networkx as nx
import time
from sqlalchemy.ext.declarative import DeclarativeMeta
from tqdm import tqdm

from bio2bel import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.dsl import BaseEntity
from pybel.struct.utils import relabel_inplace
from pybel.constants import FUNCTION, FUSION, IDENTIFIER, MEMBERS, NAME, NAMESPACE, REACTANTS, VARIANTS
from pybel.dsl import FUNC_TO_DSL
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .models import Base, Concept, Descriptor, Term, Tree
from .parsers import get_descriptors, get_supplementary_records

__all__ = [
    'Manager',
]

log = logging.getLogger(__name__)


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Bio2BEL MeSH manager."""

    module_name = MODULE_NAME
    flask_admin_models = [Descriptor, Concept, Term, Tree]

    namespace_model = Descriptor
    identifiers_recommended = 'MeSH'
    identifiers_pattern = '^(C|D)\d{6}$'
    identifiers_miriam = 'MIR:00000560'
    identifiers_namespace = 'mesh'
    identifiers_url = 'http://identifiers.org/mesh/'

    @property
    def _base(self) -> DeclarativeMeta:
        return Base

    def is_populated(self) -> bool:
        """Check if the database is already populated."""
        return 0 < self.count_terms()

    def count_descriptors(self) -> int:
        """Count the number of descriptors in the database."""
        return self._count_model(Descriptor)

    def list_descriptors(self) -> List[Descriptor]:
        """List the descriptors from the database."""
        return self._list_model(Descriptor)

    def get_descriptor_by_ui(self, ui: str) -> Optional[Descriptor]:
        """Get a descriptor by its UI, if it exists."""
        return self.session.query(Descriptor.descriptor_ui == ui).one_or_none()

    def get_descriptor_by_name(self, name: str) -> Optional[Descriptor]:
        """Get a descriptor by its name, if it exists."""
        return self.session.query(Descriptor.name == name).one_or_none()

    def count_concepts(self) -> int:
        """Count the number of concepts in the database."""
        return self._count_model(Concept)

    def list_concepts(self) -> List[Concept]:
        """List the concepts from the database."""
        return self._list_model(Concept)

    def get_concept_by_ui(self, ui) -> Optional[Concept]:
        """Get a concept by its UI, if it exists."""
        return self.session.query(Concept.concept_ui == ui).one_or_none()

    def count_terms(self) -> int:
        """Count the number of terms in the database."""
        return self._count_model(Term)

    def list_terms(self) -> List[Term]:
        """List the terms from the database."""
        return self._list_model(Term)

    def get_term_by_ui(self, ui: str) -> Optional[Term]:
        """Get a term by its UI, if it exists."""
        return self.session.query(Term.term_ui == ui).one_or_none()

    def get_term_by_name(self, name: str) -> Optional[Term]:
        """Get a term by its name, if it exists."""
        return self.session.query(Term).filter(Term.name == name).one_or_none()

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(
            terms=self.count_terms(),
            concepts=self.count_concepts(),
            descriptors=self.count_descriptors()
        )

    def populate(self) -> None:
        """Populate the database."""
        self._populate_descriptors()

    def _populate_supplement(self) -> None:
        log.info('getting supplementary xml')
        get_supplementary_records()
        log.error('_populate_supplement needs to be implemented!')

    def _populate_descriptors(self) -> None:
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

    @staticmethod
    def _get_identifier(model: Descriptor) -> str:
        return model.descriptor_ui

    def _create_namespace_entry_from_model(self, model: Descriptor, namespace: Namespace) -> NamespaceEntry:
        if model.is_pathology:
            encoding = 'O'
        elif model.is_process:
            encoding = 'B'
        elif model.is_chemical:
            encoding = 'A'
        else:
            encoding = None  # no idea. don't validate

        return NamespaceEntry(
            namespace=namespace,
            name=model.name,
            identifier=model.descriptor_ui,
            encoding=encoding,
        )

    def look_up_node(self, data) -> Optional[Descriptor]:
        namespace = data.get(NAMESPACE)
        if namespace is None or not namespace.lower().startswith('mesh'):
            return

        name, identifier = data.get(NAME), data.get(IDENTIFIER)

        if identifier:
            return self.get_descriptor_by_ui(identifier)

        term = self.get_term_by_name(name)
        if term:
            return term.concept.descriptor

    def iter_nodes(self, graph: BELGraph) -> Iterable[Tuple[BaseEntity, Descriptor]]:
        for _, node_data in graph.nodes(data=True):
            descriptor = self.look_up_node(node_data)
            if descriptor is not None:
                yield node_data, descriptor

    def normalize_terms(self, graph: BELGraph) -> Counter:
        """Add identifiers to all MeSH terms and return a counter of the namespaces fixed."""
        self.add_namespace_to_graph(graph)

        mapping = {}
        fixed_namespaces = []

        for node_data, term in self.iter_nodes(graph):
            node_tuple = node_data.as_tuple()
            if any(x in node_data for x in (VARIANTS, MEMBERS, REACTANTS, FUSION)):
                log.info('skipping: %s', node_tuple)
                continue

            fixed_namespaces.append(node_data[NAMESPACE])
            dsl = FUNC_TO_DSL[node_data[FUNCTION]]

            node = dsl(
                namespace='mesh',
                name=term.name,
                identifier=term.descriptor_ui,
            )
            graph._node[node_tuple] = node
            mapping[node_tuple] = node.as_tuple()

        relabel_inplace(graph, mapping)

        return Counter(fixed_namespaces)
