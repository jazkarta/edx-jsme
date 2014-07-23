"""
Adds input and response types for JSME problems.
"""
import json
import re

from capa import inputtypes, responsetypes
from capa.correctmap import CorrectMap


@inputtypes.registry.register
class JSMEInput(inputtypes.InputTypeBase):
    """
    A JSME input type.
    """
    template = 'jsmeinput.html'
    tags = ['jsme']

    def setup(self):
        if self.value:
            stored_state = json.loads(json.loads(self.value)['state'])
        else:
            stored_state = {}

        answer = None
        state = stored_state.get('state')
        dirty = False
        for child in self.xml:
            if not child.text.strip():
                continue
            if child.tag == 'initial-state' and state is None:
                stored_state['state'] = self.read_molfile(child.text)
                dirty = True
            elif child.tag == 'answer':
                answer = child.text
                if answer != stored_state.get('answer'):
                    stored_state['answer'] = answer
                    dirty = True

        if not answer:
            raise ValueError("Must provide an answer.")

        if dirty:
            self.value = json.dumps(
                {'answer': '', 'state': json.dumps(stored_state)});

    def read_molfile(self, text):
        lines = filter(None, text.split('\n'))
        padding = re.search(r"\S", lines[0]).start()
        return '\n'.join((line[padding:] for line in lines))

    def _extra_context(self):
        static_url = self.capa_system.STATIC_URL
        return {
            'html_file': static_url + 'jsme_frame.html',
            'params': None,
            'gradefn': 'getGrade',
            'get_statefn': 'getState',
            'set_statefn': 'setState',
            'width': '700',
            'height': '350',
            'jschannel_loader': '{static_url}js/capa/src/jschannel.js'.format(
                static_url=static_url),
            'jsinput_loader': '{static_url}js/capa/src/jsinput.js'.format(
                static_url=static_url),
            'saved_state': self.value
        }


@responsetypes.registry.register
class JSMEResponse(responsetypes.LoncapaResponse):
    """
    A JSME response type.
    """
    allowed_inputfields = ['jsme']
    required_attributes = []
    tags = ['jsmeresponse']
    max_inputfields = 1
    correct_answer = []

    def get_answers(self):
        elements = self.xml.xpath("./answer")
        if elements:
            answer = elements[0].text.strip()
        else:
            answer = ''
        return {self.answer_id: answer}

    def get_score(self, student_answers):
        graded_answer = json.loads(
            student_answers[self.answer_id].strip())['answer']
        return CorrectMap(self.answer_id, graded_answer)

