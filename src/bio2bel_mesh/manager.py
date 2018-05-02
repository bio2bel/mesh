# -*- coding: utf-8 -*-

"""Bio2BEL MeSH manager."""

from bio2bel import AbstractManager
from .constants import MODULE_NAME
from .models import Base
from .parsers import get_descriptors, get_supplement

__all__ = [
    'Manager',
]


class Manager(AbstractManager):
    """Bio2BEL MeSH manager."""

    module_name = MODULE_NAME

    @property
    def _base(self):
        return Base

    def is_populated(self):
        raise NotImplementedError

    def populate(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_cli(cls):
        main = super().get_cli()

        @main.command()
        def download():
            """Download and mock-parse everything"""
            get_descriptors()
            get_supplement()
            
        return main
