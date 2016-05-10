"""
Tests for JSME problem type.
"""
import os
import json
import mock
from mock import Mock
import unittest

import yaml
from lxml import etree

from . import JSMEInput, JSMEResponse


def mock_capa_module():
    """
    capa response types needs just two things from the capa_module: location and track_function.
    """
    capa_module = Mock()
    capa_module.location.to_deprecated_string.return_value = 'i4x://Foo/bar/mock/abc'
    return capa_module


class JSMEInputTests(unittest.TestCase):
    """
    Test JSMEInput
    """
    xml = etree.fromstring("""
        <jsme id="foo">
          <initial-state>
            Some molfile
              Testing
              1 2 3
          </initial-state>
          <answer>foo</answer>
        </jsme>
        """)

    def test_setup(self):
        """
        Test that molfile data is extracted properly from XML.
        """
        system = mock.Mock()
        obj = JSMEInput(system, self.xml, {})
        obj.setup()
        value = json.loads(obj.value)
        state = json.loads(value['state'])
        self.assertEqual(state['answer'], 'foo')
        self.assertEqual(state['state'], u'Some molfile\n  Testing\n  1 2 3\n')

    def test_setup_noanswer(self):
        """
        Test failure to provide an answer in XML.
        """
        system = mock.Mock()
        xml = etree.fromstring('<jsme id="foo"></jsme>')
        with self.assertRaises(Exception) as context:
            JSMEInput(system, xml, {})
        self.assertTrue("Must provide an answer." in str(context.exception))

    def test_setup_blank_molfile_with_whitespace(self):
        """
        Test that molfile data that is empty except for whitespace is properly
        parsed.
        """
        system = mock.Mock()
        xml = etree.fromstring(
            '<jsme id="foo"><initial-state> </initial-state>'
            '<answer>foo</answer></jsme>')
        obj = JSMEInput(system, xml, {})
        obj.setup()
        value = json.loads(obj.value)
        state = json.loads(value['state'])
        self.assertEqual(state['answer'], 'foo')
        self.assertTrue('state' not in state)

    def test_extra_context(self):
        """
        Test that _extra_context is properly populated.
        """
        system = mock.Mock(STATIC_URL='/static/')
        obj = JSMEInput(system, self.xml, {})
        obj.setup()
        self.assertEqual(obj._extra_context(), {
            'set_statefn': 'setState',
            'height': '350',
            'html_file': '/static/jsme_frame.html',
            'get_statefn': 'getState',
            'gradefn': 'getGrade',
            'jsinput_loader': '/static/js/capa/src/jsinput.js',
            'saved_state': '{"answer": "", "state": "{\\"answer\\": \\"foo\\",'
                           ' \\"state\\": \\"Some molfile\\\\n  Testing\\\\n  '
                           '1 2 3\\\\n\\"}"}',
            'width': '700',
            'params': None,
            'jschannel_loader': '/static/js/capa/src/jschannel.js'})


class JSMEResponseTests(unittest.TestCase):
    """
    Test JSMEResponse
    """
    xml = etree.fromstring("""
        <jsmeresponse>
          Foo
          <answer>One</answer>
          <answer>Two</answer>
        </jsmeresponse>
        """)

    def test_get_answers(self):
        """
        Test method `check_string`.
        """
        system = mock.Mock()
        input_fields = [JSMEInputTests.xml]
        obj = JSMEResponse(self.xml, input_fields, {}, system, mock_capa_module())
        self.assertEqual(obj.get_answers(), {'foo': 'One'})

    def test_get_score(self):
        system = mock.Mock()
        input_fields = [JSMEInputTests.xml]
        obj = JSMEResponse(self.xml, input_fields, {}, system, mock_capa_module())
        student_answers = {'foo': json.dumps({'answer': 'bar'})}
        score = obj.get_score(student_answers)
        self.assertEqual(score['foo']['correctness'], 'bar')


class JSMEOLXFormatTests(unittest.TestCase):
    """
    Test JSME OLX format
    """
    def test_question_olx_format(self):
        """
        Test that in olx question data is inside <question></question> tags.
        """
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'problem')
        with open('{}/jsme.yaml'.format(base_path)) as jsme_yaml:
            template = jsme_yaml.read()
        template = yaml.safe_load(template)

        root = etree.fromstring(template.get('data'))
        childs = [child.tag for child in root.getchildren()]
        self.assertEqual(set(childs), set(['question']))
