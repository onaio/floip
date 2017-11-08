floip-py
========

A library for converting the questions in a FLOIP Data Package descriptor to an
ODK XForm.

Getting Started
---------------

::

    $ pip install -e "git+git://github.com/onaio/floip-py.git@master"
    $ floip data/flow-results-example-1.json


Example
^^^^^^^

Reading a FLOIP results data package and generating the XML ODK XForm.

.. code:: python

    from floip import FloipSurvey
    suvey = FloipSurvey('data/flow-results-example-1.json')
    print(survey.xml())

Documentation
-------------

FloipSurvey
^^^^^^^^^^^

A class that converts a FLOIP results data package to an ODK XForm.
