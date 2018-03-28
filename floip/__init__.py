# -*- coding=utf-8 -*-
"""
FLOIP utility functions.
"""
import codecs
import json
import re

import six
from datapackage import Package
from pyxform import Survey, constants
from pyxform.builder import create_survey_element_from_dict

try:
    from json.decoder import JSONDecodeError  # pylint: disable=C0412
except ImportError:
    # python2 does not have JSONDecodeError, it raises a ValueError if
    # it is not a valid JSON string.
    JSONDecodeError = ValueError

SELECT_QUESTION = [constants.SELECT_ONE, constants.SELECT_ALL_THAT_APPLY]

NUMERIC = 'numeric'

QUESTION_TYPES = {
    'audio': 'audio',
    'date': 'date',
    'datetime': 'dateTime',
    'geo_point': 'geopoint',
    'image': 'image',
    NUMERIC: 'integer',
    'select_one': constants.SELECT_ONE,
    'select_many': constants.SELECT_ALL_THAT_APPLY,
    'text': 'text',
    'open': 'text',
    'time': 'time',
    'video': 'video'
}

FLOIP_QUESTION_TYPES = {
    'audio': 'audio',
    'calculate': 'calculate',
    'date': 'date',
    'dateTime': 'datetime',
    'geopoint': 'geo_point',
    'image': 'image',
    'integer': NUMERIC,
    constants.SELECT_ONE: 'select_one',
    constants.SELECT_ALL_THAT_APPLY: 'select_many',
    'text': 'text',
    'time': 'time',
    'video': 'video'
}

FLOW_RESULTS_PROFILE = 'flow-results-package'


class ValidationError(Exception):
    """
    ValidationError exception class.
    """
    pass


def floip_dict_from_xform_dict(question_dict):
    """
    Converts a XForm question dictionary to a FLOIP question dictionary.
    """
    question_type = FLOIP_QUESTION_TYPES[question_dict['type']]
    type_options = {}
    question = {'type': question_type}
    if 'label' in question_dict:
        question['label'] = question_dict['label']
    bind = question_dict.get('bind')
    if question_type == NUMERIC and bind and bind.get('constraint'):
        constraint = bind['constraint']
        is_range = len(constraint.split('and'))
        if is_range:
            type_options['range'] = [
                v for v in map(int, re.findall(r'\d+', constraint))
            ]
    if question_type in ['select_one', 'select_many']:
        if question_dict['children']:
            type_options['choices'] = [
                choice['name'] for choice in question_dict['children']
            ]
    if question_type == 'calculate' and bind:
        type_options['calculate'] = bind['calculate']
    question['type_options'] = type_options
    return question


def survey_questions(questions):
    """
    Returns an iterator of floip questions from XForm questions.
    """
    for question in questions:
        if question['type'] not in ['group', 'repeat']:
            try:
                yield (question['name'], floip_dict_from_xform_dict(question))
            except KeyError:
                continue
        else:
            for _key, _value in survey_questions(question['children']):
                yield '/'.join([question['name'], _key]), _value


def survey_to_floip_package(survey, flow_id, created, modified, data=None):
    """
    Takes an XForm suvey object and generates the equivalent Floip Descriptor
    file.
    """
    descriptor = {
        # 'profile': 'flow-results-package',
        'profile': 'data-package',
        'name': survey['id_string'],
        "flow_results_specification_version": "1.0.0-rc1",
        "created": created,
        "modified": modified,
        "id": flow_id,
        'title': survey['title'],
        "resources": [{
            "path": data,
            "name": survey["id_string"] + '-data',
            "mediatype": "application/json",
            "encoding": "utf-8",
            "schema": {
                "language": "eng",
                "fields": [{
                    "name": "timestamp",
                    "title": "Timestamp",
                    "type": "datetime"
                }, {
                    "name": "row_id",
                    "title": "Row ID",
                    "type": "string"
                }, {
                    "name": "contact_id",
                    "title": "Contact ID",
                    "type": "string"
                }, {
                    "name": "question_id",
                    "title": "Question ID",
                    "type": "string"
                }, {
                    "name": "response",
                    "title": "Response",
                    "type": "any"
                }, {
                    "name": "response_metadata",
                    "title": "Response Metadata",
                    "type": "object"
                }],
                "questions": {
                    name: question
                    for name, question in survey_questions(survey['children'])
                }
            }
        }]
    }  # yapf: disable

    return Package(descriptor)


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
    if question_type in SELECT_QUESTION:
        question_dict['choices'] = [{
            'label': x,
            'name': x
        } for x in options['choices']]
    if options and 'range' in options:
        assert len(options['range']) > 1, "range requires atleast two values."
        start, end = options['range'][0], options['range'][1]
        constraint = '. >= %(start)s and . <= %(end)s' % {
            'start': start,
            'end': end
        }
        if 'bind' not in question_dict:
            question_dict['bind'] = {}
        question_dict['bind'].update({'constraint': constraint})
    question = create_survey_element_from_dict(question_dict)
    survey.add_child(question)

    return question


class FloipSurvey(object):
    """
    Converter of a FLOIP Result descriptor to Openrosa XForm.
    """

    def __init__(self, descriptor=None, title=None, id_string=None):
        # Seek to begining of file if it has the seek attribute before loading
        # the file.
        if hasattr(descriptor, 'seek'):
            descriptor.seek(0)
        try:
            # descriptor is a file
            self.descriptor = json.load(descriptor)
        except AttributeError:
            try:
                # descriptor is a JSON string
                self.descriptor = json.loads(descriptor)
            except JSONDecodeError:
                # descriptor is a file path.
                self.descriptor = json.load(
                    codecs.open(descriptor, encoding='utf-8'))

        if self.descriptor['profile'] == FLOW_RESULTS_PROFILE:
            del self.descriptor['profile']

        self._package = Package(self.descriptor)
        self.descriptor = self._package.descriptor
        self._name = id_string or self._package.descriptor.get('name')
        assert self._name, "The 'name' property must be defined."
        title = title or self._package.descriptor.get('title') or self._name
        survey_dict = {
            constants.NAME: 'data',
            constants.ID_STRING: self._name,
            constants.TITLE: title,
            constants.TYPE: constants.SURVEY,
        }
        self._survey = Survey(**survey_dict)
        self.build()

    def build(self):
        """
        Creates the survey questions for the XForm a FLOIP descriptor.
        """
        if not self._package.resources:
            raise ValidationError("At least one data resource is required.")

        resource = self._package.resources[0]
        if 'schema' not in resource.descriptor:
            raise ValidationError("The 'schema' object is missing in resource")
        if 'questions' not in resource.descriptor['schema']:
            raise ValidationError(
                "The 'questions' object is missing from schema")

        questions = resource.descriptor['schema']['questions']
        if isinstance(questions, dict):
            question_keys = list(questions.keys())
            question_keys.sort()
            for name in question_keys:
                xform_from_floip_dict(self._survey, name, questions[name])
        elif isinstance(questions, list):
            for question in questions:
                for name in question:
                    xform_from_floip_dict(self._survey, name, question[name])
        else:
            raise ValidationError(
                "Expecting 'questions' to be an object or array")

        self._survey.validate()
        # check that we can recreate the survey object from the survey JSON
        create_survey_element_from_dict(self._survey.to_json_dict())

    @property
    def survey(self):
        """
        Returns a pyxform `Survey` object
        """
        return self._survey

    def xml(self):
        """
        Returns a XForm XML
        """
        return self._survey.to_xml()

    def survey_dict(self):
        """
        Returns a XForm dict.
        """
        return self._survey.to_json_dict()
