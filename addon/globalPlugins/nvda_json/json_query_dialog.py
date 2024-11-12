import json

import ui

import jsonpath_ng
import jsonpath_ng.ext
import wx

from .abstract import JsonManipulatorDialog

class JsonQueryDialog(JsonManipulatorDialog):
    def __init__(self, parent, text, multi):
        super(JsonQueryDialog, self).__init__(parent, text, title = 'JSON Query')
        self.label_manipulation_expression.SetLabel('JSONPath expression')
        self.multi = multi
        self.set_output(self.parse_text(self.text, self.multi))

    def manipulate(self, event):
        expression = self.manipulation_expression.GetValue().strip()
        try:
            jsonpath = jsonpath_ng.ext.parse(expression)
            data = json.loads(self.parse_text(self.text, self.multi))
            matches = [match.value for match in jsonpath.find(data)]
            if matches:
                matches = matches[0] if (len(matches) == 1 and isinstance(matches[0], list)) else matches
                self.set_output(self.format_json(matches))
            else:
                ui.message('No matches found')
        except (jsonpath_ng.exceptions.JsonPathLexerError, jsonpath_ng.exceptions.JsonPathParserError) as e:
            ui.message(f'JSONPath Expression Error: {str(e)}')
