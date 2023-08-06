

.. image:: ./assets/logo.png
   :target: ./assets/logo.png
   :alt: FlakeHell

===============================================================================


.. image:: https://badge.fury.io/py/flakehell.svg
   :target: https://badge.fury.io/py/flakehell
   :alt: PyPI version


.. image:: https://cloud.drone.io/api/badges/life4/flakehell/status.svg
   :target: https://cloud.drone.io/life4/flakehell
   :alt: Build Status


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT


.. image:: https://readthedocs.org/projects/flakehell/badge/?version=latest
   :target: https://flakehell.readthedocs.io/
   :alt: Documentation


It's a `Flake8 <https://gitlab.com/pycqa/flake8>`_ wrapper to make it cool.


* `Lint md, rst, ipynb, and more <https://flakehell.readthedocs.io/parsers.html>`_.
* `Shareable and remote configs <https://flakehell.readthedocs.io/config.html#base>`_.
* `Legacy-friendly <https://flakehell.readthedocs.io/commands/baseline.html>`_\ : ability to get report only about new errors.
* Caching for much better performance.
* `Use only specified plugins <https://flakehell.readthedocs.io/config.html#plugins>`_\ , not everything installed.
* `Make output beautiful <https://flakehell.readthedocs.io/formatters.html>`_.
* `pyproject.toml <https://www.python.org/dev/peps/pep-0518/>`_ support.
* `Check that all required plugins are installed <https://flakehell.readthedocs.io/commands/missed.html>`_.
* `Syntax highlighting in messages and code snippets <https://flakehell.readthedocs.io/formatters.html#colored-with-source-code>`_.
* `PyLint <https://github.com/PyCQA/pylint>`_ integration.
* `Remove unused noqa <https://flakehell.readthedocs.io/commands/dropqa.html>`_.
* `Powerful GitLab support <https://flakehell.readthedocs.io/formatters.html#gitlab>`_.
* Codes management:

  * Manage codes per plugin.
  * Enable and disable plugins and codes by wildcard.
  * `Show codes for installed plugins <https://flakehell.readthedocs.io/commands/plugins.html>`_.
  * `Show all messages and codes for a plugin <https://flakehell.readthedocs.io/commands/codes.html>`_.
  * Allow codes intersection for different plugins.


.. image:: ./assets/grouped.png
   :target: ./assets/grouped.png
   :alt: output example


Compatibility
-------------

FlakeHell supports all flake8 plugins, formatters, and configs. However, FlakeHell has it's own beautiful way to configure enabled plugins and codes. So, options like ``--ignore`` and ``--select`` unsupported. You can have flake8 and FlakeHell in one project if you want but enabled plugins should be explicitly specified.

Installation
------------

.. code-block:: bash

   python3 -m pip install --user flakehell

Usage
-----

First of all, let's create ``pyproject.toml`` config:

.. code-block::

   [tool.flakehell]
   # optionally inherit from remote config (or local if you want)
   base = "https://raw.githubusercontent.com/life4/flakehell/master/pyproject.toml"
   # specify any flake8 options. For example, exclude "example.py":
   exclude = ["example.py"]
   # make output nice
   format = "grouped"
   # 80 chars aren't enough in 21 century
   max_line_length = 90
   # show line of source code in output
   show_source = true

   # list of plugins and rules for them
   [tool.flakehell.plugins]
   # include everything in pyflakes except F401
   pyflakes = ["+*", "-F401"]
   # enable only codes from S100 to S199
   flake8-bandit = ["-*", "+S1??"]
   # enable everything that starts from `flake8-`
   "flake8-*" = ["+*"]
   # explicitly disable plugin
   flake8-docstrings = ["-*"]

Show plugins that aren't installed yet:

.. code-block:: bash

   flakehell missed

Show installed plugins, used plugins, specified rules, codes prefixes:

.. code-block:: bash

   flakehell plugins


.. image:: ./assets/plugins.png
   :target: ./assets/plugins.png
   :alt: plugins command output


Show codes and messages for a specific plugin:

.. code-block:: bash

   flakehell codes pyflakes


.. image:: ./assets/codes.png
   :target: ./assets/codes.png
   :alt: codes command output


Run flake8 against the code:

.. code-block:: bash

   flakehell lint

This command accepts all the same arguments as Flake8.

Read `flakehell.readthedocs.io <https://flakehell.readthedocs.io/>`_ for more information.

Contributing
------------

Contributions are welcome! A few ideas what you can contribute:


* Improve documentation.
* Add more tests.
* Improve performance.
* Found a bug? Fix it!
* Made an article about FlakeHell? Great! Let's add it into the ``README.md``.
* Don't have time to code? No worries! Just tell your friends and subscribers about the project. More users -> more contributors -> more cool features.

A convenient way to run tests is using `DepHell <https://github.com/dephell/dephell>`_\ :

.. code-block:: bash

   curl -L dephell.org/install | python3
   dephell venv create --env=pytest
   dephell deps install --env=pytest
   dephell venv run --env=pytest

Bug-tracker is disabled by-design to shift contributions from words to actions. Please, help us make the project better and don't stalk maintainers in social networks and on the street.

Thank you :heart:


.. image:: ./assets/flaky.png
   :target: ./assets/flaky.png
   :alt: 


The FlakeHell mascot (Flaky) is created by `@illustrator.way <https://www.instagram.com/illustrator.way/>`_ and licensed under the `CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_ license.
