Donfig
======

.. image:: https://github.com/pytroll/donfig/workflows/CI/badge.svg?branch=master
    :target: https://github.com/pytroll/donfig/actions?query=workflow%3A%22CI%22

.. image:: https://codecov.io/gh/pytroll/donfig/branch/master/graph/badge.svg?token=xmvNtxzdoB
   :target: https://codecov.io/gh/pytroll/donfig

.. image:: https://anaconda.org/conda-forge/donfig/badges/version.svg
   :target: https://anaconda.org/conda-forge/donfig/

Donfig is a python library meant to make configuration easier for other
python packages. Donfig can be configured programmatically, by
environment variables, or from YAML files in standard locations. The
below examples show the basics of using donfig. For more details see the
official `documentation <https://donfig.readthedocs.io/en/latest/>`_.

Installation
------------

Donfig can be installed from PyPI using pip:

.. code-block:: bash

    pip install donfig

Or with conda using the conda-forge channel:

.. code-block:: bash

    conda install -c conda-forge donfig

Using Donfig
------------

Create the package-wide configuration object for your package named `mypkg`:

.. code-block:: python

    # mypkg/__init__.py
    from donfig import Config
    config = Config('mypkg')

Use the configuration object:

.. code-block:: python

    from mypkg import config
    important_val = config.get('important_key')
    if important_val:
        # do something
    else:
        # something else

Set configuration in Python
---------------------------

Configuration can be modified in python before code using it is called:

.. code-block:: python

    # mypkg/work.py
    from mypkg import config
    config.set(important_key=5)

    # use the configuration

Donfig configurations can also be changed as a context manager:

.. code-block:: python

    config.set(other_key=True)

    with config.set(other_key=False):
        print(config.get('other_key'))  # False

    print(config.get('other_key'))  # True

Configure from environment variables
------------------------------------

Environment variables are automatically loaded when the Config object is
created. Any environment variable starting with the name of the config
object in all capital letters and an underscore will be loaded in to
the config object:

.. code-block:: bash

    export MYPKG_MY_KEY="a value"

And can be accessed in python:

.. code-block:: python

    from mypkg import config
    print(config.get('my_key'))

Configure from YAML file
------------------------

Donfig will also automatically load any YAML configuration files found in
specific paths. The default paths:

- ~/.config/<config name>/
- /etc/<config name>/
- <sys.prefix>/etc/<config name>/

Note the `/etc/<config name>/` directory can also be specified with the
environment variable `DASK_ROOT_CONFIG`. Also note that
`~/.config/<package name>` (or other location specified with `DASK_CONFIG`)
can be created as a custom user configuration file for easier user
customization (see documentation for details).

History
-------

Donfig is based on the original configuration logic of the `dask` library.
The code has been modified to use a config object instead of a global
configuration dictionary. This makes the configuration logic of dask available
to everyone. The name "donfig" is a shortening of "dask.config", the original
dask module that implemented this functionality.

License
-------

Original code from the dask library was distributed under the license
specified in `DASK_LICENSE.txt`. In November 2018 this code was migrated to
the Donfig project under the MIT license described in `LICENSE.txt`. The full
copyright for this project is therefore::

    Copyright (c) 2018 Donfig Developers
    Copyright (c) 2014-2018, Anaconda, Inc. and contributors
