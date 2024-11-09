import json

import api
import ui

import jsonpath_ng
import jsonpath_ng.ext
import wx

from .abstract import Dialog as AbstractDialog

class JsonQueryDialog(AbstractDialog):
    def __init__(self, parent, text, multi):
        super(JsonQueryDialog, self).__init__(parent, text, title = 'JSON Query')
        self.multi = multi
        self.originalText.SetValue(text)
        self.set_output(self.parse_text(self.text, self.multi))

    def set_output(self, output):
        self.output.SetValue(output if output is not None else '')

    def create_ui(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        jsonSizer = wx.BoxSizer(wx.VERTICAL)
        originalTextLabel = wx.StaticText(self, label = "Original text")
        self.originalText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        jsonSizer.Add(originalTextLabel)
        jsonSizer.Add(self.originalText, 1, wx.EXPAND | wx.ALL, 5)
        pathExpressionLabel = wx.StaticText(self, label="Path Expression")
        self.pathExpression = wx.TextCtrl(self, style=wx.TE_LEFT|wx.TE_PROCESS_ENTER )
        jsonSizer.Add(pathExpressionLabel)
        jsonSizer.Add(self.pathExpression, 0, wx.EXPAND | wx.ALL, 5)
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
        self.pathExpression.Bind(wx.EVT_TEXT_ENTER, self.on_path_expression_enter)

    def on_copy_output_click(self, event):
        copied = api.copyToClip(self.output.GetValue())
        if copied:
            ui.message('Copied')
        else:
            ui.message('Error when copying')

    def on_path_expression_enter(self, event):
        expression = self.pathExpression.GetValue().strip()
        try:
            jsonpath_expr = jsonpath_ng.ext.parse(expression)
            json_data = json.loads(self.parse_text(self.text, self.multi))
            matches = [match.value for match in jsonpath_expr.find(json_data)]
            if matches:
                matches = matches[0] if len(matches) == 1 else matches
                self.set_output(self.format_json(matches))
            else:
                ui.message('No matches found')
        except (jsonpath_ng.exceptions.JsonPathLexerError, jsonpath_ng.exceptions.JsonPathParserError) as e:
            ui.message(f'JSONPath Expression Error: {str(e)}')
