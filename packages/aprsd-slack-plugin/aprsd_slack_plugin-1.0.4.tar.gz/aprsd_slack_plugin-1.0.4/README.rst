aprsd_slack_plugin
==================

.. image:: https://github.com/hemna/aprsd-slack-plugin/workflows/python/badge.svg
    :target: https://github.com/hemna/aprsd-slack-plugin/actions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://timothycrosley.github.io/isort/

This project is a python plugin for the APRSD server daemon written by
Craig Lamparter.   The plugin looks for location APRS commands from a ham
radio, then reports that location to a slack channel.  This is basically a
location proxy.

Requirements
------------

Python 3.6+.
APRSD - http://github.com/craigerl/aprsd

.. note::

    Because `Python 2.7 supports ended January 1, 2020 <https://pythonclock.org/>`_, new projects
    should consider supporting Python 3 only, which is simpler than trying to support both.
    As a result, support for Python 2.7 in this example project has been dropped.
