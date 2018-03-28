pyfloip
=======


|travis| |codacy|

.. |travis| image:: https://travis-ci.org/onaio/floip-py.svg?branch=master
            :target: https://travis-ci.org/onaio/floip-py
            :alt: Travis

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/ab2327b86a7d4445875aebd4dd632d05
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/ukanga/floip-py?utm_source=github.com&utm_medium=referral&utm_content=onaio/floip-py&utm_campaign=badger

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
