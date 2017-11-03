# -*- coding=utf-8 -*-
"""
FLOIP utility functions.
"""

from datapackage import Package

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

    def __init__(self, descriptor=None, title=None, id_string=None):
        self._package = Package(descriptor)
        self._name = id_string or self._package.descriptor.get('name')
        assert self._name, "The 'name' property must be defined."
        title = title or self._package.descriptor.get('title') or self._name
        self._survey = Survey(name='data', id_string=self._name, title=title)
        self.build()

    def build(self):
        """Creates the survey questions for the XForm a FLOIP descriptor.
        """
        data_resource_name = self._name + '-data'
        resource = self._package.get_resource(data_resource_name)
        if not resource:
            raise ValueError(
                "The data resource '{name}' is not defined.".format(
                    name=data_resource_name))
        assert 'schema' in resource.descriptor
        assert 'questions' in resource.descriptor['schema']

        questions = resource.descriptor['schema']['questions']

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
