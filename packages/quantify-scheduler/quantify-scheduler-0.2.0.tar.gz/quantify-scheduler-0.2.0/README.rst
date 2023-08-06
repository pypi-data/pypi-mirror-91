==================
quantify-scheduler
==================

.. image:: https://gitlab.com/quantify-os/quantify-scheduler/badges/develop/pipeline.svg
    :target: https://gitlab.com/quantify-os/quantify-scheduler/pipelines/

.. image:: https://img.shields.io/pypi/v/quantify-scheduler.svg
    :target: https://pypi.org/pypi/quantify-scheduler

.. image:: https://gitlab.com/quantify-os/quantify-scheduler/badges/develop/coverage.svg
    :target: https://gitlab.com/quantify-os/quantify-scheduler/pipelines/

.. image:: https://readthedocs.com/projects/quantify-quantify-scheduler/badge/?version=latest&token=ed6fdbf228e1369eacbeafdbad464f6de927e5dfb3a8e482ad0adcbea76fe74c
    :target: https://quantify-quantify-scheduler.readthedocs-hosted.com/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-BSD%204--Clause-blue.svg
    :target: https://gitlab.com/quantify-os/quantify-scheduler/-/blob/master/LICENSE



Quantify is a python based data acquisition platform focused on Quantum Computing and solid-state physics experiments.
It is build on top of `QCoDeS <https://qcodes.github.io/Qcodes/>`_ and is a spiritual successor of `PycQED <https://github.com/DiCarloLab-Delft/PycQED_py3>`_.
Quantify currently consists of `quantify-core <https://pypi.org/project/quantify-core/>`_ and `quantify-scheduler <https://pypi.org/project/quantify-scheduler/>`_.

Quantify-scheduler is a module for writing quantum programs. It features a unique hybrid control model allowing quantum gate- and pulse-level descriptions to be combined in a clearly defined and hardware-agnostic way. Quantify-scheduler is designed to allow experimentalists to easily define complex experiments, and produces synchronized pulse schedules to be distributed to control hardware.

.. caution::

    This is a pre-release **alpha version**, major changes are expected. Use for testing & development purposes only.

About
--------

Quantify-scheduler is maintained by The Quantify consortium consisting of Qblox and Orange Quantum Systems.

.. |_| unicode:: 0xA0
   :trim:


.. figure:: https://cdn.sanity.io/images/ostxzp7d/production/f9ab429fc72aea1b31c4b2c7fab5e378b67d75c3-132x31.svg
    :width: 200px
    :target: https://qblox.com
    :align: left

.. figure:: https://orangeqs.com/OQS_logo_with_text.svg
    :width: 200px
    :target: https://orangeqs.com
    :align: left

|_|


|_|

The software is free to use under the conditions specified in the license.


--------------------------
