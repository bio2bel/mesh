# -*- coding: utf-8 -*-

"""Utilities for Bio2BEL MeSH."""

import json
import logging
from typing import Iterable, TextIO

from .constants import VERSION

log = logging.getLogger(__name__)


def get_version() -> str:
    """Get the version of Bio2BEL MeSH."""
    return VERSION


def get_names(file: TextIO, tree_prefix: str) -> Iterable[str]:
    """Iterate over the names that match the given tree prefix.

    :param file: The file containing Sumit-MeSH-JSON
    :param tree_prefix: The prefix to keep
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
