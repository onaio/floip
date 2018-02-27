# -*- coding=utf-8 -*-
"""
Test floip utility functions."
"""

import codecs
import json

import pytest
from pyxform import Survey

from floip import (FloipSurvey, ValidationError, floip_dict_from_xform_dict,
                   survey_questions, survey_to_floip_package,
                   xform_from_floip_dict)


def test_geopoint_question_to_xform():
    """
    Test geo_point floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54db', {
        "type": "geo_point",
        "label": "Where are you?",
        "type_options": {}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="geopoint"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_geopoint_question_to_floip():
    """
    Test geopoint question to FLOIP geo_point dictionary.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(survey, 'ae54db', {
        "type": "geo_point",
        "label": "Where are you?",
        "type_options": {}
    })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "geo_point",
        "label": "Where are you?",
        "type_options": {}
    }


def test_numeric_question_to_xform():
    """
    Test numeric floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "numeric",
            "label": "How much do you weigh, in lbs?",
            "type_options": {}
        })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="int"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_numeric_question_to_floip():
    """
    Test numeric floip queston to XForm.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "numeric",
            "label": "How much do you weigh, in lbs?",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "numeric",
        "label": "How much do you weigh, in lbs?",
        "type_options": {}
    }

def test_numeric_range_q_to_xform():
    """
    Test numeric range floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "numeric",
            "label": "How much do you weigh, in lbs?",
            "type_options": {
                "range": [1, 250]
            }
        })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind constraint=". &gt;= 1 and . &lt;= 250" '
                u'nodeset="/floip/%(name)s" type="int"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_numeric_range_q_to_floip():
    """
    Test XForm numeric range queston to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "numeric",
            "label": "How much do you weigh, in lbs?",
            "type_options": {
                "range": [1, 250]
            }
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "numeric",
        "label": "How much do you weigh, in lbs?",
        "type_options": {
            "range": [1, 250]
        }
    }



def test_select_one_q_to_xform():
    """
    Test select_one floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d4', {
        "type": "select_one",
        "label": "Are you male or female?",
        "type_options": {
            "choices": ["male", "female", "not identified"]
        }
    })
    choices = [
        '<item><label>male</label><value>male</value></item>',
        '<item><label>female</label><value>female</value></item>',
        '<item><label>not identified</label><value>not identified</value>'
        '</item>'
    ]
    expected_data = {
        'name': question['name'],
        'label': question['label'],
        'choices': ''.join(choices)
    }
    body_xml = (
        u'<select1 ref="/floip/%(name)s"><label>%(label)s</label>%(choices)s'
        u'</select1>' % expected_data)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="select1"/>' % question)
    assert question.xml_binding().toxml() == bind_xml
    assert len([child.xml() for child in question.children]) == 3


def test_select_one_q_to_floip():
    """
    Test XForm select_one question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "select_one",
            "label": "Are you male or female?",
            "type_options": {
                "choices": ["male", "female", "not identified"]
            }
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "select_one",
        "label": "Are you male or female?",
        "type_options": {
            "choices": ["male", "female", "not identified"]
        }
    }


def test_select_many_q_to_xform():
    """
    Test select_many floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d5', {
        "type": "select_many",
        "label": "What is your favorite desert?",
        "type_options": {
            "choices": ["cake", "fruit", "ice cream"]
        }
    })
    choices = [
        '<item><label>cake</label><value>cake</value></item>',
        '<item><label>fruit</label><value>fruit</value></item>',
        '<item><label>ice cream</label><value>ice cream</value>'
        '</item>'
    ]
    expected_data = {
        'name': question['name'],
        'label': question['label'],
        'choices': ''.join(choices)
    }
    body_xml = (
        u'<select ref="/floip/%(name)s"><label>%(label)s</label>%(choices)s'
        u'</select>' % expected_data)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="select"/>' % question)
    assert question.xml_binding().toxml() == bind_xml
    assert len([child.xml() for child in question.children]) == 3


def test_select_many_q_to_floip():
    """
    Test XForm select_many question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "select_many",
            "label": "What is your favorite desert?",
            "type_options": {
                "choices": ["cake", "fruit", "ice cream"]
            }
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "select_many",
        "label": "What is your favorite desert?",
        "type_options": {
            "choices": ["cake", "fruit", "ice cream"]
        }
    }


def test_text_question_to_xform():
    """
    Test text floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d6', {
        "type": "text",
        "label": "What is your name?",
        "type_options": {}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="string"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_text_question_to_floip():
    """
    Test XForm text queston to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "text",
            "label": "What is your name?",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "text",
        "label": "What is your name?",
        "type_options": {}
    }


def test_image_upload_to_xform():
    """
    Test an image floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(
        survey, 'ae54d7', {
            "type": "image",
            "label": "Upload an image of your location",
            "type_options": {}
        })
    body_xml = (u'<upload mediatype="image/*" ref="/floip/%(name)s">'
                '<label>%(label)s</label></upload>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="binary"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_image_upload_to_floip():
    """
    Test an XForm image question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "image",
            "label": "Upload an image of your location",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "image",
        "label": "Upload an image of your location",
        "type_options": {}
    }


def test_audio_upload_to_xform():
    """
    Test an audio floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d8', {
        "type": "audio",
        "label": "Upload an audio recording",
        "type_options": {}
    })
    body_xml = (u'<upload mediatype="audio/*" ref="/floip/%(name)s">'
                '<label>%(label)s</label></upload>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="binary"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_audio_upload_to_floip():
    """
    Test XForm audio question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "audio",
            "label": "Upload an audio recording",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "audio",
        "label": "Upload an audio recording",
        "type_options": {}
    }


def test_video_upload_to_xform():
    """
    Test a video floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d9', {
        "type": "video",
        "label": "Upload a video recording",
        "type_options": {}
    })
    body_xml = (u'<upload mediatype="video/*" ref="/floip/%(name)s">'
                '<label>%(label)s</label></upload>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="binary"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_video_upload_to_floip():
    """
    Test XForm video question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "video",
            "label": "Upload a video recording",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "video",
        "label": "Upload a video recording",
        "type_options": {}
    }


def test_date_question_to_xform():
    """
    Test a floip date question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d10', {
        "type": "date",
        "label": "What is the date?",
        "type_options": {}
    })
    body_xml = (u'<input ref="/floip/%(name)s">'
                '<label>%(label)s</label></input>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="date"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_date_question_to_floip():
    """
    Test XForm date question to FLOIP
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "date",
            "label": "What is the date?",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "date",
        "label": "What is the date?",
        "type_options": {}
    }


def test_time_question_to_xform():
    """
    Test a floip time question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d10', {
        "type": "time",
        "label": "What is the time?",
        "type_options": {}
    })
    body_xml = (u'<input ref="/floip/%(name)s">'
                '<label>%(label)s</label></input>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="time"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_time_question_to_floip():
    """
    Test XForm time question to FLOIP
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "time",
            "label": "What is the time?",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "time",
        "label": "What is the time?",
        "type_options": {}
    }


def test_date_time_q_to_xform():
    """
    Test a floip dateTime question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d10', {
        "type": "datetime",
        "label": "What is the date and time?",
        "type_options": {}
    })
    body_xml = (u'<input ref="/floip/%(name)s">'
                '<label>%(label)s</label></input>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="dateTime"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_date_time_q_to_floip():
    """
    Test XForm datetime question to FLOIP.
    """
    survey = Survey(name='floip')
    element = xform_from_floip_dict(
        survey, 'ae54d8', {
            "type": "datetime",
            "label": "What is the date and time?",
            "type_options": {}
        })
    question = floip_dict_from_xform_dict(element.to_json_dict())
    assert question == {
        "type": "datetime",
        "label": "What is the date and time?",
        "type_options": {}
    }


def test_xform_group_to_floip():
    """
    Test a group question to floip.
    """
    group = {
        "control": {
            "bodyless": True
        },
        "children": [
            {
                "name": "instanceID",
                "bind": {
                    "readonly": "true()",
                    "calculate": "concat('uuid:', uuid())"
                },
                "type": "calculate"
            }
        ],
        "name": "meta",
        "type": "group"
    }
    question = list(survey_questions([group]))
    assert question == [('meta/instanceID', {
        "type": "calculate",
        "type_options": {
            "calculate": "concat('uuid:', uuid())"
        }
    })]


def test_floip_descriptor_to_xform():
    """
    Test FloipSurvey - converting a flow result descriptor to an XForm xml.
    """
    survey = FloipSurvey('data/flow-results-example-1.json')
    with codecs.open('data/flow-results-example-1.xml') as xform_file:
        assert survey.xml() == xform_file.read()


def test_xform_to_floip_descriptor():
    """
    Test FloipSurvey - converting a flow result descriptor to an XForm xml.
    """
    survey = FloipSurvey('data/flow-results-example-1.json')
    with codecs.open('data/flow-results-example-1.xml') as xform_file:
        assert survey.xml() == xform_file.read()

    with codecs.open('data/flow-results-example-1.json') as descriptor_file:
        package = survey_to_floip_package(
            survey.survey_dict(), survey.descriptor['id'],
            survey.descriptor['created'], survey.descriptor['modified'],
            'data/flow-results-example-1-data.json')
        assert package.descriptor == json.load(descriptor_file)
        assert package.valid is True


def test_floip_descriptor_to_xform_questions_as_list(): # pylint: disable=C0103
    """
    Test FloipSurvey - converting a flow result descriptor to an XForm xml when
    resource questions is a list.
    """
    with pytest.raises(ValidationError,
                       match=r"Expecting 'questions' to be an object"):
        FloipSurvey('data/flow-results-example-2.json')
