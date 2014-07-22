"""
Adds input and response types for JSDraw problems.
"""
import json
import re

from capa import inputtypes, responsetypes
from capa.correctmap import CorrectMap


@inputtypes.registry.register
class JSDrawInput(inputtypes.InputTypeBase):
    """
    A JSDraw input type.
    """
    template = 'jsdrawinput.html'
    tags = ['jsdraw']

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
                answer = self.read_molfile(child.text)
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
        padding = re.search(r"\S", lines[1]).start() - 1
        return '\n'.join(
            (lines[0],) + tuple(line[padding:] for line in lines[1:]))

    def _extra_context(self):
        static_url = self.capa_system.STATIC_URL
        return {
            'html_file': static_url + 'jsdraw_frame.html',
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
class JSDrawResponse(responsetypes.LoncapaResponse):
    """
    A JSDraw response type.
    """
    allowed_inputfields = ['jsdraw']
    required_attributes = []
    tags = ['jsdrawresponse']
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

