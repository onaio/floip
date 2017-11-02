# -*- coding=utf-8 -*-
"""
FLOIP utility functions.
"""

from pyxform.builder import create_survey_element_from_dict

QUESTION_TYPES = {
    "multiple_choice": "select_one",
    "numeric": "integer",
    "open": "text",
    "geo_point": "geopoint"
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
    question = create_survey_element_from_dict(question_dict)
    survey.add_child(question)

    return question
