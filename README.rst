|PyPI| |Build Status| |codecov.io|

===
EAF
===

Enterprise Application Framework.

This framework contains all the pieces you need to create feature-rich
enterprise-grade distributed and distributedn't applications.

Also means Extensible As Fuck.

Requirements
============

* >=python-3.7
* >=tornado-6.0

Installation
============

.. code-block:: console

	$ pip install eaf


Development
===========

Installation
------------

.. code-block:: console

   $ poetry install

Testing
-------

.. code-block:: console

   $ poetry run pytest -s -v tests/  # run all tests
   $ poetry run pytest --cov=eaf -s -v tests/  # run all tests with coverage
   $ poetry run black eaf/ tests/  # autoformat code
   $ # run type checking
   $ poetry run pytest --mypy --mypy-ignore-missing-imports -s -v eaf/ tests/
   $ # run code linting
   $ poetry run pytest --pylint -s -v eaf/ tests/

Documentation
-------------

* **To be added**

.. |PyPI| image:: https://badge.fury.io/py/eaf.svg
   :target: https://badge.fury.io/py/eaf
.. |Build Status| image:: https://github.com/pkulev/eaf/workflows/CI/badge.svg
.. |codecov.io| image:: http://codecov.io/github/pkulev/eaf/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/eaf?branch=master
