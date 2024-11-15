import json

import config
import ui

import jsonpath_ng
import jsonpath_ng.ext
import wx

from .abstract import JsonManipulatorDialog

class JsonQueryDialog(JsonManipulatorDialog):
    query_engines = {
        'jq': {
            'edit_label': 'JQ Expression',
            'handler': 'parse_jq',
        },
        'jsonpath': {
            'edit_label': 'JSONPath Expression',
            'handler': 'parse_jsonpath',
        }
    }

    def __init__(self, parent, text, multi):
        super(JsonQueryDialog, self).__init__(parent, text, title = 'JSON Query')
        self.query_engine = JsonQueryDialog.query_engines[config.conf['json']['query_engine']]
        self.label_manipulation_expression.SetLabel(self.query_engine['edit_label'])
        self.multi = multi
        self.set_output(self.parse_text(self.text, self.multi))

    def manipulate(self, event):
        expression = self.manipulation_expression.GetValue().strip()
        matches = getattr(self, self.query_engine['handler'])(expression)
        if matches:
            matches = matches[0] if (len(matches) == 1 and isinstance(matches[0], list)) else matches
            self.set_output(self.format_json(matches))
        else:
            ui.message('No matches found')

    def parse_jsonpath(self, expression):
        try:
            jsonpath = jsonpath_ng.ext.parse(expression)
            data = json.loads(self.parse_text(self.text, self.multi))
            return [match.value for match in jsonpath.find(data)]
        except (jsonpath_ng.exceptions.JsonPathLexerError, jsonpath_ng.exceptions.JsonPathParserError) as e:
            ui.message(f'JSONPath Expression Error: {str(e)}')

    def parse_jq(self, expression):
        ui.message('Not implemented')
