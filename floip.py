# -*- coding=utf-8 -*-
"""
FLOIP utility functions.
"""

import codecs
import json
import os

import six

from pyxform import Survey, constants
from pyxform.builder import create_survey_element_from_dict

MULTIPLE_CHOICE = 'multiple_choice'

QUESTION_TYPES = {
    MULTIPLE_CHOICE: constants.SELECT_ONE,
    'numeric': 'integer',
    'open': 'text',
    'geo_point': 'geopoint'
}


def xform_from_floip_dict(survey, name, values):
    """
    Creates an XForm SurveyElement from FLOIP Result questions specification.

    survey - a pyxform Survey object
    name   - the floip question name or uuid
    values - the floip question object with the type, label and question
             options for the question.
    """
    question_type = QUESTION_TYPES[values['type']]
    question_dict = {
        'name': name,
        'label': values['label'],
        'type': question_type
    }
    options = values.get('type_options')
    if question_type == constants.SELECT_ONE:
        question_dict['choices'] = [
            {'label': x, 'name': x} for x in options['choices']]
    if options and 'range' in options:
        assert len(options['range']) > 1, "range requires atleast two values."
        start, end = options['range'][0], options['range'][1]
        constraint = '. >= %(start)s and . <= %(end)s' % {'start': start,
                                                          'end': end}
        if 'bind' not in question_dict:
            question_dict['bind'] = {}
        question_dict['bind'].update({'constraint': constraint})
    question = create_survey_element_from_dict(question_dict)
    survey.add_child(question)

    return question


class FloipSurvey(object):
    """Converter of a FLOIP Result descriptor to Openrosa XForm.
    """

    def __init__(self, name, descriptor=None, title=None, id_string=None):
        title = name if title is None else title
        id_string = name if id_string is None else id_string
        self._survey = Survey(name=name, id_string=id_string, title=title)

        if isinstance(descriptor, six.string_types):
            if os.path.isfile(descriptor):
                with codecs.open(descriptor) as descriptor_file:
                    self.descriptor = json.load(descriptor_file)
                    self.build()

    def build(self):
        """Creates the survey questions for the XForm a FLOIP descriptor.
        """
        assert hasattr(self, 'descriptor')
        assert 'resources' in self.descriptor

        resources = self.descriptor['resources']
        num_resources = len(resources)
        assert isinstance(resources, list) and num_resources
        assert 'schema' in resources[0]
        assert 'questions' in resources[0]['schema']

        questions = resources[0]['schema']['questions']

        for name, values in questions.items():
            xform_from_floip_dict(self._survey, name, values)

        self._survey.validate()

    @property
    def survey(self):
        """Returns a pyxform `Survey` object
        """
        return self._survey

    def xml(self):
        """Returns a XForm XML
        """
        return self._survey.to_xml()
