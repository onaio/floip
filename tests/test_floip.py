# -*- coding=utf-8 -*-
"""
Test floip utility functions."
"""

import codecs

from floip import FloipSurvey, xform_from_floip_dict
from pyxform import Survey


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


def test_numeric_question_to_xform():
    """
    Test numeric floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d8', {
        "type": "numeric",
        "label": "How much do you weigh, in lbs?",
        "type_options": {}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="int"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_numeric_range_q_to_xform():
    """
    Test numeric range floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d8', {
        "type": "numeric",
        "label": "How much do you weigh, in lbs?",
        "type_options": {"range": [1, 250]}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind constraint=". &gt;= 1 and . &lt;= 250" '
        u'nodeset="/floip/%(name)s" type="int"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


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


def test_image_upload_to_xform():
    """
    Test an image floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d7', {
        "type":
        "image",
        "label":
        "Upload an image of your location",
        "type_options": {}
    })
    body_xml = (u'<upload mediatype="image/*" ref="/floip/%(name)s">'
                '<label>%(label)s</label></upload>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="binary"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


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


def test_video_upload_to_xform():
    """
    Test an audio floip question to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d9', {
        "type": "video",
        "label": "Upload an audio recording",
        "type_options": {}
    })
    body_xml = (u'<upload mediatype="video/*" ref="/floip/%(name)s">'
                '<label>%(label)s</label></upload>' % question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (u'<bind nodeset="/floip/%(name)s" type="binary"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


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


def test_floip_survey():
    """
    Test FloipSurvey class
    """
    survey = FloipSurvey('data/flow-results-example-1.json')
    with codecs.open('data/flow-results-example-1.xml') as xform_file:
        assert survey.xml() == xform_file.read()
