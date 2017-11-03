# -*- coding=utf-8 -*-
"""
FLOIP utility functions.
"""

from pyxform.builder import create_survey_element_from_dict
from pyxform import constants

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
