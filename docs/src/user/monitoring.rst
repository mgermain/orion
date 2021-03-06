**********
Monitoring
**********

You can monitor the experiments and their results using either the command line, the python API or
the REST API. The command line tools help monitoring the status of experiments and inspect available
experiments in a database. The library API can also be used to query the database within python
code. Finally, the REST API facilitates the integration of the experiments' results with third party
tools.

Commands for terminal
=====================

.. _cli-info:
.. include:: cli/list.rst
.. include:: cli/status.rst
.. include:: cli/info.rst

Library API
===========

.. _library-api-results:
.. include:: library/results.rst

.. _library-api-evc-results:
.. include:: library/evc_results.rst

REST API
========

.. _rest-api:
.. include:: rest_api.rst
