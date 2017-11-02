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
