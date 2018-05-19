# -*- coding: utf-8 -*-

import click

from .manager import Manager

main = Manager.get_cli()


@main.group()
def manage():
    pass


@manage.group()
def terms():
    pass


@terms.command()
@click.argument('q')
@click.pass_obj
def search(manager, q):
    model = manager.get_term_by_name(q)

    if model is not None:
        for k, v in model.to_json().items():
            click.echo(f'{k}: {v}')


if __name__ == '__main__':
    main()
