# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dmarc_metrics_exporter',
 'dmarc_metrics_exporter.model',
 'dmarc_metrics_exporter.model.tests',
 'dmarc_metrics_exporter.tests']

package_data = \
{'': ['*']}

install_requires = \
['aioimaplib>=0.7.18,<0.8.0',
 'dataclasses-serialization>=1.3.1,<2.0.0',
 'prometheus_client>=0.9.0,<0.10.0',
 'uvicorn[standard]>=0.13.2,<0.14.0',
 'xsdata>=20.12,<21.0']

setup_kwargs = {
    'name': 'dmarc-metrics-exporter',
    'version': '0.2.3',
    'description': 'Export Prometheus metrics from DMARC reports.',
    'long_description': '.. image:: https://travis-ci.com/jgosmann/dmarc-metrics-exporter.svg?branch=main\n  :target: https://travis-ci.com/jgosmann/dmarc-metrics-exporter\n  :alt: Travis-CI build\n.. image:: https://codecov.io/gh/jgosmann/dmarc-metrics-exporter/branch/main/graph/badge.svg?token=O4M05YWNQK\n  :target: https://codecov.io/gh/jgosmann/dmarc-metrics-exporter\n  :alt: Codecov coverage\n.. image:: https://img.shields.io/pypi/v/dmarc-metrics-exporter\n  :target: https://pypi.org/project/dmarc-metrics-exporter/\n  :alt: PyPI\n.. image:: https://img.shields.io/pypi/pyversions/dmarc-metrics-exporter\n  :target: https://pypi.org/project/dmarc-metrics-exporter/\n  :alt: PyPI - Python Version\n.. image:: https://img.shields.io/pypi/l/dmarc-metrics-exporter\n  :target: https://pypi.org/project/dmarc-metrics-exporter/\n  :alt: PyPI - License\n\ndmarcs-metrics-exporter\n=======================\n\nExport metrics derived from DMARC aggregate reports to Prometheus.\nThis exporter regularly polls\nfor new aggregate report emails\nvia IMAP.\nThe following metrics will be collected\nand exposed at an HTTP endpoint\nfor Prometheus:\n\n* ``dmarc_total``: Total number of reported messages.\n* ``dmarc_compliant_total``: Total number of DMARC compliant messages.\n* ``dmarc_quarantine_total``: Total number of quarantined messages.\n* ``dmarc_reject_total``: Total number of rejected messages.\n* ``dmarc_spf_aligned_total``: Total number of SPF algined messages.\n* ``dmarc_spf_pass_total``: Total number of messages with raw SPF pass.\n* ``dmarc_dkim_aligned_total``: Total number of DKIM algined messages.\n* ``dmarc_dkim_pass_total``: Total number of messages with raw DKIM pass.\n\nEach of these metrics is subdivided by the following labels:\n\n* ``reporter``: Domain from which a DMARC aggregate report originated.\n* ``from_domain``: Domain from which the evaluated email originated.\n* ``dkim_domain``: Domain the DKIM signature is for.\n* ``spf_domain``: Domain used for the SPF check.\n\n\nInstallation\n------------\n\nThis describes the manual setup fo dmarc-metrics-exporter.\nAn Ansible role for automated deployment is provided in ``roles``.\nFurther instructions for Ansible are given in the readme file\nprovided in that directory.\n\nIt is best to run dmarc-metrics-exporter under a separate system user account.\nCreate one for example with\n\n.. code-block:: bash\n\n    adduser --system --group dmarc-metrics\n\nThen you can install dmarc-metrics-exporter with ``pip`` from PyPI for that\nuser:\n\n.. code-block:: bash\n\n    sudo -u dmarc-metrics pip3 install dmarc-metrics-exporter\n\nYou will need a location to store the ``metrics.db`` that is writable by that\nuser, for example:\n\n.. code-block:: bash\n\n    mkdir /var/lib/dmarc-metrics-exporter\n    chown dmarc-metrics:dmarc-metrics /var/lib/dmarc-metrics-exporter\n\n\nConfiguration\n-------------\n\nTo run dmarc-metrics-exporter a configuration file in JSON format is required.\nThe default location is ``/etc/dmarc-metrics-exporter.json``.\n\nBecause the configuration file will contain the IMAP password,\nmake sure to ensure proper permissions on it,\nfor example:\n\n.. code-block:: bash\n\n    chown root:dmarc-metrics /etc/dmarc-metrics-exporter.json\n    chmod 640 /etc/dmarc-metrics-exporter.json\n\nAn example configuration file is provided in this repository in\n``config/dmarc-metrics-exporter.sample.json``.\n\nThe following configuration options are available:\n\n* ``listen_addr`` (string, default ``"127.0.0.1"``): Listen address for the HTTP endpoint.\n* ``port`` (number, default ``9119``): Port to listen on for the HTTP endpoint.\n* ``imap`` (object, required): IMAP configuration to check for aggregate reports.\n\n  * ``host`` (string, default ``"localhost"``): Hostname of IMAP server to connect to.\n  * ``port`` (number, default ``993``): Port of the IMAP server to connect to.\n  * ``username`` (string, required): Login username for the IMAP connection.\n  * ``password``: (string, required): Login password for the IMAP connection.\n\n* ``folders`` (object):\n\n  * ``inbox`` (string, default ``"INBOX"``): IMAP mailbox that is checked for incoming DMARC aggregate reports.\n  * ``done`` (string, default ``"Archive"``): IMAP mailbox that successfully processed reports are moved to.\n  * ``error``: (string, default ``"Invalid"``): IMAP mailbox that emails are moved to that could not be processed.\n\n* ``metrics_db`` (string, default ``"/var/lib/dmarc-metrics-exporter/metrics.db"``):\n  File to persist accumulated metrics information in.\n* ``poll_interval_seconds`` (number, default ``60``): How often to poll the IMAP server in seconds.\n\nUsage\n-----\n\nTo run dmarc-metrics-exporter with the default configuration in\n``/etc/dmarc-metrics-exporter.json``:\n\n.. code-block:: bash\n\n    sudo -u dmarc-metrics python3 -m dmarc_metrics_exporter\n\nTo use a different configuration file:\n\n.. code-block:: bash\n\n    sudo -u dmarc-metrics python3 -m dmarc_metrics_exporter --configuration <path>\n\n\nsystemd\n^^^^^^^\n\nInstead of manually starting the dmarc-metrics-exporter,\nyou likely want to have it run as a system service.\nAn example systemd service file is provided in this repository in\n``config/dmarc-metrics-exporter.service``.\nMake sure that the paths and user/group names match your configuration\nand copy it to ``/etc/systemd/system`` to use it.\nTo have systemd pick it up a ``systemctl daemon-reload`` might be necessary.\n\nYou can than start/stop dmarc-metrics-exorter with:\n\n.. code-block:: bash\n\n    systemctl start dmarc-metrics-exporter\n    systemctl stop dmarc-metrics-exporter\n\nTo have dmarc-metrics-exporter start on system boot:\n\n.. code-block:: bash\n\n    systemctl enable dmarc-metrics-exporter\n',
    'author': 'Jan Gosmann',
    'author_email': 'jan@hyper-world.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jgosmann/dmarc-metrics-exporter/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
