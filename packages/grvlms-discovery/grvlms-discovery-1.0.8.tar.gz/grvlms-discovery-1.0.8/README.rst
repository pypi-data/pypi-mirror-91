Discovery plugin for `Grvlms <https://docs.grvlms.groove.education>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/groovetch/grvlms-discovery

Usage
-----

::

    grvlms plugins enable discovery
    grvlms discovery config -i (Interative Mode)
    grvlms config save
    grvlms local quickstart
    
Configuration
-------------

- ``DISCOVERY_INDEX_NAME`` (default: ``"catalog"``)
- ``DISCOVERY_MYSQL_DATABASE`` (default: ``"discovery"``)
- ``DISCOVERY_MYSQL_USERNAME`` (default: ``"discovery"``)
- ``DISCOVERY_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``DISCOVERY_SECRET_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``DISCOVERY_OAUTH2_KEY`` (default: ``"discovery"``)
- ``DISCOVERY_OAUTH2_KEY_DEV`` (default: ``"discovery-dev"``)
- ``DISCOVERY_OAUTH2_SECRET`` (default: ``"{{ 8|random_string }}"``)

Release Note 1.0.8
------------------

- hotfix/EDT-339-fixing-template

Release Note 1.0.7
------------------

- EDT-339-fixing-template

License
-------

This software is licensed under the terms of the AGPLv3.