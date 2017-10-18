# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os
import sys

import click

from .convert import download, load_store_from_pickle, rdf_to_pickle, mesh_to_nx, process_mesh
from .convert_sumit import write_names, get_names

log = logging.getLogger(__name__)
logging.basicConfig(level=10, format='%(asctime)s %(name)s:%(levelname)s - %(message)s')
log.setLevel(10)


@click.group()
def main():
    """Tools for dealing with Sumit-MeSH-JSON"""


@main.command()
@click.option('--directory', default=os.path.expanduser('~/Desktop'))
@click.option('--output', type=click.File('w'), default=sys.stdout, help='Output path OWL')
def make_owl(directory, output):
    from owlready import to_owl

    log.info('start loading')

    default_store_path = os.path.join(directory, 'mesh.nt')
    default_pickle_path = os.path.join(directory, 'mesh.pickle')

    if not os.path.exists(default_store_path):
        download(default_store_path)

    if os.path.exists(default_pickle_path):
        s = load_store_from_pickle(default_pickle_path)
    else:
        s = rdf_to_pickle(default_store_path)

    log.info('done loading. starting conversion to nx')

    g = mesh_to_nx(s)

    log.info('done converting to nx. starting conversion to owl')

    o = process_mesh(g)

    log.info('done converting to owl. outputting')

    click.echo(to_owl(o), file=output)

    log.info('done outputting')


@main.command()
@click.option('--input', type=click.File('r'), default=sys.stdin, help="Input MESH JSON from sumit")
@click.option('--output', type=click.File('w'), default=sys.stdout, help='Output path OWL')
@click.option('--tree', default='D')
def make_belns(input, output, tree):
    write_names(input, output, tree)


@main.command()
@click.option('-f', '--file', type=click.File('r'), default=sys.stdin, help="Input MESH JSON from sumit")
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout, help='Output path for names')
@click.option('--tree', default='D')
def ls(input, output, tree):
    """Lists the names matching a given tree prefix"""
    for name in get_names(input, tree):
        click.echo(name, file=output)


if __name__ == '__main__':
    main()
