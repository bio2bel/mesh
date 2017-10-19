# -*- coding: utf-8 -*-

"""This file takes in the mesh.json that sumit makes and outputs a BEL namespace with those terms"""

import json
import logging

from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel_tools.definition_utils import write_namespace
from .utils import get_names
log = logging.getLogger(__name__)





def write_names(in_file, out_file, tree):
    """

    :param file in_file:
    :param file out_file:
    :param str tree:
    :return:
    """
    write_namespace(
        namespace_name='MESH{}'.format(tree),
        namespace_keyword='MESH{}'.format(tree),
        namespace_description='A namespace from MeSH entries starting with {}'.format(tree),
        namespace_domain='Other',
        author_name='Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        citation_name='MeSH',
        values=get_names(in_file, tree),
        cacheable=True,
        file=out_file,
    )




def write_meshc(in_file, out_file):
    """Writes the MeSH [C] Diseases to a BEL Namespace"""
    write_namespace(
        namespace_name='MESHC',
        namespace_keyword='MESHC',
        namespace_description="MeSH Diseases",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        citation_name='MeSH',
        values=get_names(in_file, 'C'),
        cacheable=True,
        functions='O',
        file=out_file,
    )


if __name__ == '__main__':
    import os

    owncloud_base = os.environ['OWNCLOUD_BASE']
    bel_resource_base = os.environ['PYBEL_RESOURCES_BASE']
    in_path = os.path.join(owncloud_base, 'mesh.json')

    meshf_out_path = os.path.join(bel_resource_base, 'meshf.belns')

    with open(in_path) as in_file, open(meshf_out_path, 'w') as out_file:
        write_mesh_f_belns(in_file, out_file)

    meshc_out_path = os.path.join(bel_resource_base, 'meshc.belns')

    with open(in_path) as in_file, open(meshc_out_path, 'w') as out_file:
        write_meshc(in_file, out_file)

        # for tree in 'FK':
        #
        #
        #    with open(in_path) as in_file, open(out_path, 'w') as out_file:
        #        write_names(in_file, out_file, tree)
