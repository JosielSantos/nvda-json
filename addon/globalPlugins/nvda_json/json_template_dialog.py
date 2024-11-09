import json

import ui

import jsonpointer
import wx

from .abstract import JsonManipulatorDialog

class JsonTemplateDialog(JsonManipulatorDialog):
    def __init__(self, parent, text):
        super(JsonTemplateDialog, self).__init__(parent, text, title = 'JSON template')
        self.label_manipulation_expression.SetLabel('Template')
        self.original_text.SetValue(text)

    def manipulate(self, event):
        template = self.manipulation_expression.GetValue().strip()
        data = json.loads(self.parse_text(self.text, False))
        self.set_output(self.parse_template(data, template))

    def parse_template(self, data, template):
        result = ''
        escape = False
        i = 0
        while i < len(template):
            if template[i] == "\\":
                escape = True
                i += 1
                continue
            if template[i] == '{' and not escape:
                end_index = template.find('}', i)
                if end_index != -1:
                    pointer = template[i + 1:end_index]
                    try:
                        value = jsonpointer.resolve_pointer(data, pointer)
                        result += str(value)
                    except jsonpointer.JsonPointerException:
                        result += '{' + pointer + '}'
                    i = end_index + 1
                    continue
            if escape:
                result += template[i]
                escape = False
            else:
                result += template[i]
            i += 1
        return result
