# -*- coding: utf-8 -*-

import json
import logging
import os

log = logging.getLogger(__name__)

owncloud_base = os.environ.get('OWNCLOUD_BASE')
mesh_json_path = os.path.join(owncloud_base, 'mesh.json') if owncloud_base else None


def get_names(file, tree_prefix):
    """Iterates over the names that match the given tree prefix

    :param file file: The file containing Sumit-MeSH-JSON
    :param str tree_prefix: The prefix to keep
    :rtype: iter[str]
    """
    d = json.load(file)

    for i, entry in enumerate(d):
        if 'name' not in entry:
            continue

        name = entry['name']

        if 'treeNumbers' not in entry:
            log.debug('Missing tree from %s', name)
            continue

        if not any(tree.startswith(tree_prefix) for tree in entry['treeNumbers']):
            continue

        yield name