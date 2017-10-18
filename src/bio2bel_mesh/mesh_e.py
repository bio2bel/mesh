# -*- coding: utf-8 -*-

import os

from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel_tools.definition_utils import write_namespace

from bio2bel_mesh.utils import get_names, mesh_json_path


def write_mesh_e_belns(in_file, out_file):
    """Writes the MeSH [E] Analytical stuff to a BEL Namespace"""
    write_namespace(
        namespace_name='Analytical, Diagnostic and Therapeutic Techniques and Equipment Category',
        namespace_keyword='MESHE',
        namespace_description="MeSH Diseases",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        citation_name='MeSH',
        values=get_names(in_file, 'E'),
        cacheable=True,
        file=out_file,
    )


if __name__ == '__main__':
    with open(mesh_json_path) as in_f, open(os.path.expanduser('~/Desktop/meshe.belns'), 'w') as out_f:
        write_mesh_e_belns(in_f, out_f)
