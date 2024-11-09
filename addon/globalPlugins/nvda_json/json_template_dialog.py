import json

import api
import ui

import jsonpointer
import wx

from .abstract import Dialog as AbstractDialog

class JsonTemplateDialog(AbstractDialog):
    def __init__(self, parent, text):
        super(JsonTemplateDialog, self).__init__(parent, text, title = 'JSON template')
        self.originalText.SetValue(text)

    def set_output(self, output):
        self.output.SetValue(output if output is not None else '')

    def create_ui(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        jsonSizer = wx.BoxSizer(wx.VERTICAL)
        originalTextLabel = wx.StaticText(self, label = "Original text")
        self.originalText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        jsonSizer.Add(originalTextLabel)
        jsonSizer.Add(self.originalText, 1, wx.EXPAND | wx.ALL, 5)
        templateLabel = wx.StaticText(self, label="Template")
        self.template = wx.TextCtrl(self, style=wx.TE_LEFT|wx.TE_PROCESS_ENTER )
        jsonSizer.Add(templateLabel)
        jsonSizer.Add(self.template, 0, wx.EXPAND | wx.ALL, 5)
        outputLabel = wx.StaticText(self, label="Output")
        self.output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        jsonSizer.Add(outputLabel)
        jsonSizer.Add(self.output, 1, wx.EXPAND | wx.ALL, 5)
        copyOutputButton = wx.Button(self, label="Copy output to clipboard")
        copyOutputButton.Bind(wx.EVT_BUTTON, self.on_copy_output_click)
        jsonSizer.Add(copyOutputButton, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        mainSizer.Add(jsonSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        self.template.Bind(wx.EVT_TEXT_ENTER, self.on_template_enter)

    def on_copy_output_click(self, event):
        copied = api.copyToClip(self.output.GetValue())
        if copied:
            ui.message('Copied')
        else:
            ui.message('Error when copying')

    def on_template_enter(self, event):
        template = self.template.GetValue().strip()
        json_data = json.loads(self.parse_text(self.text, False))
        self.set_output(self.parse_template(json_data, template))

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
