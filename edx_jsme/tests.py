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
        <jsdraw id="foo">
          Some molfile
            Testing
            1 2 3
        </jsdraw>
        """)

    def test_setup(self):
        """
        Test that molfile data is extracted properly from XML.
        """
        system = mock.Mock()
        obj = JSMEInput(system, self.xml, {})
        obj.setup()
        value = json.loads(obj.value)
        self.assertEqual(value['answer'], '')
        self.assertEqual(value['state'], u'Some molfile\n  Testing\n  1 2 3\n')

    def test_setup_blank_molfile_with_whitespace(self):
        """
        Test that molfile data that is empty except for whitespace is properly
        parsed.
        """
        system = mock.Mock()
        xml = etree.fromstring('<jsdraw id="foo"> </jsdraw>')
        obj = JSMEInput(system, xml, {})
        obj.setup()
        self.assertEqual(obj.value, '')

    def test_extra_context(self):
        """
        Test that _extra_context is properly populated.
        """
        system = mock.Mock(STATIC_URL='/static/')
        obj = JSMEInput(system, self.xml, {})
        obj.setup()
        self.assertEqual(obj._extra_context(), {
            'set_statefn': 'setMolfile',
            'height': '350',
            'html_file': '/static/jsdraw_frame.html',
            'get_statefn': 'getMolfile',
            'gradefn': 'getSmiles',
            'jsinput_loader': '/static/js/capa/src/jsinput.js',
            'saved_state': '{"answer": "", "state": "Some molfile\\n  '
                           'Testing\\n  1 2 3\\n"}',
            'width': '700',
            'params': None,
            'jschannel_loader': '/static/js/capa/src/jschannel.js',
            'sop': None})


class JSMEResponseTests(unittest.TestCase):
    """
    Test JSMEResponse
    """
    xml = etree.fromstring("""
        <jsdrawresponse>
          Foo
          <answer>One</answer>
          <answer>Two</answer>
        </jsdrawresponse>
        """)

    def test_setup_response(self):
        """
        Test method `setup_response`.
        """
        system = mock.Mock()
        input_fields = [JSMEInputTests.xml]
        obj = JSMEResponse(self.xml, input_fields, {}, system)
        obj.setup_response()
        self.assertEqual(obj.correct_answer, ['One', 'Two'])

    def test_check_string(self):
        """
        Test method `check_string`.
        """
        system = mock.Mock()
        input_fields = [JSMEInputTests.xml]
        obj = JSMEResponse(self.xml, input_fields, {}, system)
        self.assertTrue(obj.check_string(['One', 'Two'], '{"answer": "One"}'))
        self.assertFalse(
            obj.check_string(['One', 'Two'], '{"answer": "Three"}'))
