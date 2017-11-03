floip-py
========

A library for converting the questions in a FLOIP Data Package descriptor to an
ODK XForm.

Getting Started
---------------

pip install -r git+git://github.com/onaio/floip-py.git@master


Example
^^^^^^^

.. code-block:: python
   :linenos:

   from floip import FloipSurvey

   suvey = FloipSurvey('data/flow-results-example-1.json')
   print(survey.xml())


FloipSurvey
^^^^^^^^^^^

A class that converts a FLOIP results data package to an ODK XForm.
