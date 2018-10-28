# -*- coding: utf-8 -*-

"""Old conversion utilities."""

import pickle
import types
from typing import Optional

import networkx as nx
import rdflib
import requests
from rdflib import Namespace, RDFS

MESH_URL = 'ftp://ftp.nlm.nih.gov/online/mesh/mesh.nt.gz'
MESH_OWL_IRI = 'http://ontologies.scai.fraunhofer.de/mesh.owl'

# See: https://meshb.nlm.nih.gov/#/treeSearch

MESH_QUERY_LABELS = """
SELECT DISTINCT ?term ?label ?treelabel
WHERE {
    ?term rdf:type <http://id.nlm.nih.gov/mesh/vocab#TopicalDescriptor> .
    ?term rdfs:label ?label .
    ?term <http://id.nlm.nih.gov/mesh/vocab#treeNumber> ?tree .
    ?tree rdfs:label ?treelabel .

    FILTER (lang(?label) = 'en') .
    FILTER STRSTARTS(?treelabel, "C") .
}
"""

MESH_DISEASE_SUBCLASS_QUERY = '''
SELECT ?child_tree_label ?parent_tree_label
WHERE
{
    ?child_tree meshv:parentTreeNumber ?parent_tree .

    ?child_tree rdfs:label ?child_tree_label .
    ?parent_tree rdfs:label ?parent_tree_label .

    FILTER (lang(?child_tree_label) = 'en') .
    FILTER (lang(?parent_tree_label) = 'en') .
    FILTER STRSTARTS(?child_tree_label, "C") .
    FILTER STRSTARTS(?parent_tree_label, "C") .
}
'''

ROOT_NAME = 'Disease'

mesh_ns = Namespace('http://id.nlm.nih.gov/mesh/')
mesh_vocab = Namespace('http://id.nlm.nih.gov/mesh/vocab#')

ns = {
    'rdfs': RDFS,
    'mesh': mesh_ns,
    'meshv': mesh_vocab
}


def download(file_path: str):
    """Download the MeSH RDF dump.

    See: http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py

    :param file_path: output file path
    """
    r = requests.get(MESH_URL, stream=True)

    r.raise_for_status()

    with open(file_path, 'w+b') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def rdf_to_pickle(file_path: str, dump_path: Optional[str] = None) -> Optional[rdflib.Graph]:
    """Parse the MeSH RDF dump with RDFLib and saves the resulting RDFLib store as a pickle object.

    :param file_path: path to MeSH RDF dump
    :param dump_path: path where to save pickled RDFLib store
    """
    store = rdflib.Graph()
    store.parse(file_path, format='nt')  # Takes about 28 minutes

    if dump_path is None:
        return store

    with open(dump_path, 'w+b') as f:
        pickle.dump(store, f)  # Takes about 3 minutes


def load_store_from_pickle(dump_path: str):
    """Load an RDFLib graph from a pickle file."""
    with open(dump_path, 'r+b') as f:
        return pickle.load(f)


def mesh_to_nx(store: rdflib.Graph) -> nx.DiGraph:
    """Serialize an RDFLib graph filled with MeSH to a NetworkX graph."""
    graph = nx.DiGraph()
    tree2term = {}

    for term, label, tree in store.query(MESH_QUERY_LABELS, initNs=ns):
        term_clean = term.rpartition('/')[2]
        tree2term[tree] = term_clean
        if term_clean not in graph:
            graph.add_node(term_clean, attr_dict={'label': str(label)})

    for child, parent in store.query(MESH_DISEASE_SUBCLASS_QUERY, initNs=ns):
        graph.add_edge(tree2term[parent], tree2term[child])

    for node in graph.nodes():
        if 0 == graph.in_degree(node):
            graph.add_edge(ROOT_NAME, node)

    graph.node[ROOT_NAME]['label'] = ROOT_NAME

    return graph


def process_mesh(graph: nx.DiGraph, iri: Optional[str] = None):
    """Process the MeSH NetworkX graph."""
    import owlready

    assert nx.is_directed_acyclic_graph(graph)

    o = owlready.Ontology(iri if iri is not None else MESH_OWL_IRI)
    kwd = {"ontology": o}

    node_cls = {
        ROOT_NAME: types.new_class(ROOT_NAME, (owlready.Thing,), kwds=kwd)
    }

    def recur(pnode):
        for neighbor in graph.successors(pnode):

            if neighbor not in node_cls:
                node_cls[neighbor] = types.new_class(neighbor, (node_cls[pnode],), kwds=kwd)
                owlready.ANNOTATIONS[node_cls[neighbor]].add_annotation(owlready.rdfs.label, graph.node[pnode]['label'])

            recur(neighbor)

    recur(ROOT_NAME)

    return o
