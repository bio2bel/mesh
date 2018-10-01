# -*- coding: utf-8 -*-

"""Command line interface for Bio2BEL MeSH."""

import click

from .manager import Manager

main = Manager.get_cli()


@main.group()
def manage():
    """Manage the database."""


@manage.group()
def descriptors():
    """Manage descriptors."""


@descriptors.command()
@click.argument('ui')
@click.pass_obj
def get(manager, ui):
    """Look up a descriptor in the database."""
    model = manager.get_descriptor_by_ui(ui)

    if model is not None:
        for k, v in model.to_json().items():
            click.echo(f'{k}: {v}')


@manage.group()
def terms():
    """Manage terms."""


@terms.command()
@click.argument('q')
@click.pass_obj
def search(manager, q):
    """Search terms in the database."""
    model = manager.get_term_by_name(q)

    if model is not None:
        for k, v in model.to_json().items():
            click.echo(f'{k}: {v}')


if __name__ == '__main__':
    main()
