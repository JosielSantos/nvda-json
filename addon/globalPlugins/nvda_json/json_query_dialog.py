import json

import config
import jq
import jsonpath_ng.ext
import ui

from .abstract import JsonManipulatorDialog


class JsonQueryDialog(JsonManipulatorDialog):
    query_engines = {
        'jq': {
            'edit_label': 'JQ Program',
            'handler': 'parse_jq',
            'type': 'jq-program',
        },
        'jsonpath': {
            'edit_label': 'JSONPath Expression',
            'handler': 'parse_jsonpath',
            'type': 'jsonpath-expression',
        }
    }

    def __init__(self, parent, text, multi):
        self.query_engine = JsonQueryDialog.query_engines[config.conf['json']['query_engine']]
        self.expression_type = self.query_engine['type']
        super().__init__(parent, text, title='JSON Query')
        self.label_manipulation_expression.SetLabel(self.query_engine['edit_label'])
        self.multi = multi
        self.set_output(self.parse_text(self.text, self.multi))

    def manipulate(self, event):
        expression = self.manipulation_expression.GetValue().strip()
        data = json.loads(self.parse_text(self.text, self.multi))
        matches = getattr(self, self.query_engine['handler'])(data, expression)
        if matches:
            matches = matches[0] if (len(matches) == 1 and isinstance(matches[0], list)) else matches
            self.set_output(self.format_json(matches))
        else:
            ui.message('No matches found')

    def parse_jsonpath(self, data, expression):
        try:
            jsonpath = jsonpath_ng.ext.parse(expression)
            return [match.value for match in jsonpath.find(data)]
        except (jsonpath_ng.exceptions.JsonPathLexerError, jsonpath_ng.exceptions.JsonPathParserError) as e:
            ui.message(f'JSONPath Expression Error: {str(e)}')
            raise e

    def parse_jq(self, data, expression):
        try:
            program = jq.compile(expression)
            return program.input(data).all()
        except Exception as e:
            ui.message(f'JQ Expression Error: {str(e)}')
            raise e
