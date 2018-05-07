Bio2BEL MeSH |build| |coverage| |documentation|
===============================================
Converts the MeSH hierarchy to BEL

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_mesh`` can be installed easily from `PyPI <https://pypi.python.org/pypi/bio2bel_mesh>`_ with the
following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_mesh

or from the latest code on `GitHub <https://github.com/bio2bel/mesh>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/mesh.git@master

Setup
-----
MeSH can be downloaded and populated from either the Python REPL or the automatically installed command line utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_mesh
    >>> mesh_manager = bio2bel_mesh.Manager()
    >>> mesh_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    bio2bel_mesh populate

Links
-----
- `MeSH Tree Browser <https://meshb.nlm.nih.gov/#/treeSearch>`_
- `SPARQL 1.1 Specification <https://www.w3.org/TR/sparql11-query/>`_
- `MeSH Information <https://id.nlm.nih.gov/mesh/>`_
- `MeSH FTP <ftp://ftp.nlm.nih.gov/online/mesh/>`_
- `MeSH RDF Download <ftp://ftp.nlm.nih.gov/online/mesh/mesh.nt.gz>`_

.. |build| image:: https://travis-ci.org/bio2bel/mesh.svg?branch=master
    :target: https://travis-ci.org/bio2bel/mesh
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/bio2bel/mesh/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/mesh?branch=master
    :alt: Coverage Status

.. |documentation| image:: https://readthedocs.org/projects/mesh/badge/?version=latest
    :target: http://mesh.readthedocs.io
    :alt: Documentation Status

.. |climate| image:: https://codeclimate.com/github/bio2bel/mesh/badges/gpa.svg
    :target: https://codeclimate.com/github/bio2bel/mesh
    :alt: Code Climate

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_mesh.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_mesh.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_mesh.svg
    :alt: MIT License
