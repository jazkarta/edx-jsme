"""
Tests for JSME problem type.
"""
import json
import mock
import unittest

from lxml import etree

from . import JSMEInput, JSMEResponse


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
        Test that molfile data is extracted properly from XML.
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
        obj = JSMEResponse(self.xml, input_fields, {}, system)
        self.assertEqual(obj.get_answers(), {'foo': 'One'})

    def test_get_score(self):
        system = mock.Mock()
        input_fields = [JSMEInputTests.xml]
        obj = JSMEResponse(self.xml, input_fields, {}, system)
        student_answers = {'foo': json.dumps({'answer': 'bar'})}
        score = obj.get_score(student_answers)
        self.assertEqual(score['foo']['correctness'], 'bar')
