pyfloip
=======

|travis|

.. |travis| image:: https://travis-ci.org/onaio/floip-py.svg?branch=master
            :target: https://travis-ci.org/onaio/floip-py

A library for converting the questions in a FLOIP Data Package descriptor to an
ODK XForm.

Getting Started
---------------

::

    $ pip install pyfloip
    $ floip data/flow-results-example-1.json

Example
^^^^^^^

Reading a FLOIP results data package and generating the XML ODK XForm.

.. code:: python

    from floip import FloipSurvey
    suvey = FloipSurvey('data/flow-results-example-1.json')
    print(survey.xml())

Testing
-------

::

    $ pip install -r requirements.txt
    $ py.test --pylint

Documentation
-------------

FloipSurvey
^^^^^^^^^^^

A class that converts a FLOIP results data package to an ODK XForm.
