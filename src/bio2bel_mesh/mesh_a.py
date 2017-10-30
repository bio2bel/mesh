# -*- coding: utf-8 -*-

import logging
import os

from bio2bel_mesh.utils import get_names, mesh_json_path
from pybel.constants import NAMESPACE_DOMAIN_OTHER
from pybel_tools.definition_utils import write_namespace
from pybel_tools.resources import deploy_namespace, get_today_arty_namespace

log = logging.getLogger(__name__)

MODULE_NAME = 'mesh-anatomy'


def write_mesh_a_belns(in_file, out_file):
    """Writes the MeSH [A] Anatomy as a BEL namespace"""
    write_namespace(
        namespace_name='Anatomy terms',
        namespace_keyword='MESHA',
        namespace_description="MeSH Anatomy",
        namespace_domain=NAMESPACE_DOMAIN_OTHER,
        author_name='Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        citation_name='MeSH',
        values=get_names(in_file, 'A'),
        cacheable=True,
        file=out_file,
    )


def deploy_to_arty(quit_fail_redeploy=True):
    """Gets the data, writes BEL namespace, and writes BEL knowledge to Artifactory"""
    if not mesh_json_path:
        raise ValueError('no mesh json avaliable')

    file_name = get_today_arty_namespace(MODULE_NAME)

    with open(mesh_json_path) as infile, open(file_name, 'w') as file:
        write_mesh_a_belns(infile, file)

    namespace_deploy_success = deploy_namespace(file_name, MODULE_NAME)

    if not namespace_deploy_success and quit_fail_redeploy:
        log.warning('did not redeploy')
        return False


if __name__ == '__main__':
    with open(mesh_json_path) as in_f, open(os.path.expanduser('~/Desktop/mesh-anatomy.belns'), 'w') as out_f:
        write_mesh_a_belns(in_f, out_f)
