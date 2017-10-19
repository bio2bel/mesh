# -*- coding: utf-8 -*-

import os

from bio2bel_mesh.utils import get_names, mesh_json_path
from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel_tools.definition_utils import write_namespace


def write_mesh_f_belns(in_file, out_file):
    """Writes the MeSH [F] Psychiatry and Psychology to a BEL Namespace"""
    write_namespace(
        namespace_name='MeSH Psychiatry and Psychology',
        namespace_keyword='MESHF',
        namespace_description="MeSH Psychiatry and Psychology",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        citation_name='MeSH',
        values=get_names(in_file, 'F'),
        cacheable=True,
        functions='OBA',
        file=out_file,
    )


if __name__ == '__main__':
    with open(mesh_json_path) as in_f, open(os.path.expanduser('~/Desktop/meshf.belns'), 'w') as out_f:
        write_mesh_f_belns(in_f, out_f)
