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

* >=python-3.10
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

   $ uv sync --extra dev

Testing
-------

.. code-block:: console

   $ poe test  # run all tests
   $ poe test --cov=eaf  # run all tests with coverage
   $ poe format [--fix]  # autoformat code
   $ poe typecheck  # run type checking
   $ poe lint [--fix]  # run code linting

Documentation
-------------

* **To be added**

.. |PyPI| image:: https://badge.fury.io/py/eaf.svg
   :target: https://badge.fury.io/py/eaf
.. |Build Status| image:: https://github.com/pkulev/eaf/workflows/CI/badge.svg
.. |codecov.io| image:: http://codecov.io/github/pkulev/eaf/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/eaf?branch=master
