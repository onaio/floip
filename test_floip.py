# -*- coding=utf-8 -*-
"""
Test floip utility functions."
"""
from floip import xform_from_floip_dict
from pyxform import Survey


def test_open_question_to_xform():
    """
    Test open/text floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54da', {
        "type": "open",
        "label": "How are you feeling today?",
        "type_options": {}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="string"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


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
        "type_options": {"range": [1, 250]}
    })
    body_xml = (
        u'<input ref="/floip/%(name)s"><label>%(label)s</label></input>' %
        question)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="int"/>' % question)
    assert question.xml_binding().toxml() == bind_xml


def test_multichoice_q_to_xform():
    """
    Test multiple_choice floip queston to XForm.
    """
    survey = Survey(name='floip')
    question = xform_from_floip_dict(survey, 'ae54d3', {
        "type": "multiple_choice",
        "label": "Are you male or female?",
        "type_options": {
            "choices": [
                "male",
                "female",
                "not identified"]}})
    choices = [
        '<item><label>male</label><value>male</value></item>',
        '<item><label>female</label><value>female</value></item>',
        '<item><label>not identified</label><value>not identified</value>'
        '</item>'
    ]
    expected_data = {'name': question['name'], 'label': question['label'],
                     'choices': ''.join(choices)}
    body_xml = (
        u'<select1 ref="/floip/%(name)s"><label>%(label)s</label>%(choices)s'
        u'</select1>' % expected_data)
    assert question.xml_control().toxml() == body_xml
    bind_xml = (
        u'<bind nodeset="/floip/%(name)s" type="select1"/>' % question)
    assert question.xml_binding().toxml() == bind_xml
    assert len([child.xml() for child in question.children]) == 3
