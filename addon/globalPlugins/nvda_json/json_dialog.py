import json

import api
import gui
import ui

import jsonpath_ng
import jsonpath_ng.ext
import wx

class JsonDialog(wx.Dialog):
    def __init__(self, parent, text, multi):
        super(JsonDialog, self).__init__(parent, title="NVDA JSON")
        self.text = text
        self.multi = multi
        self.create_ui()
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
        self.pathExpression.SetWindowStyleFlag(wx.TE_PROCESS_ENTER)

    def onKey(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def onClose(self, evt):
        self.Destroy()

    def on_copy_output_click(self, event):
        copied = api.copyToClip(self.output.GetValue())
        if copied:
            ui.message('Copied')
        else:
            ui.message('Error when copying')

    def parse_text(self, text, multi):
        if multi:
            return self.parse_text_multi(text)
        else:
            return self.parse_text_single(text)

    def parse_text_single(self, text):
        try:
            parsed_json = json.loads(text)
            return self.__format_json(parsed_json)
        except json.decoder.JSONDecodeError as error:
            return self.exit_with_error('Invalid JSON: %s' % error)

    def parse_text_multi(self, text):
        lines = filter(lambda line: line != '', map(lambda line: line.strip(), text.splitlines()))
        parsed_jsons_list = []
        for (line_number, line) in enumerate(lines):
            try:
                parsed_jsons_list.append(json.loads(line))
            except json.decoder.JSONDecodeError as error:
                return self.exit_with_error('Invalid JSON at line %d: %s' % (line_number + 1, error))
        if parsed_jsons_list == []:
            ui.message('No JSONs to display')
        return self.__format_json(parsed_jsons_list)

    def exit_with_error(self, message):
        wx.CallAfter(
            lambda: gui.messageBox(message, 'Error', wx.OK | wx.ICON_ERROR)
        )
        self.Destroy()

    def on_path_expression_enter(self, event):
        expression = self.pathExpression.GetValue().strip()
        try:
            jsonpath_expr = jsonpath_ng.ext.parse(expression)
            json_data = json.loads(self.parse_text(self.text, self.multi))
            matches = [match.value for match in jsonpath_expr.find(json_data)]
            if matches:
                matches = matches[0] if len(matches) == 1 else matches
                self.set_output(self.__format_json(matches))
            else:
                ui.message('No matches found')
        except (jsonpath_ng.exceptions.JsonPathLexerError, jsonpath_ng.exceptions.JsonPathParserError) as e:
            ui.message(f'JSONPath Expression Error: {str(e)}')

    def __format_json(self, parsed_json):
        return json.dumps(
            parsed_json,
            indent=4,
            sort_keys=True
        )
