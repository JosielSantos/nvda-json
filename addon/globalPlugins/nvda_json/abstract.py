import json
import os.path

import api
import gui
import ui

import wx

SAVED_EXPRESSIONS_FILE_NAME = os.path.dirname(__file__)+'/../../../../json-expressions.json'

class JsonManipulatorDialog(wx.Dialog):
    label_manipulation_expression = None

    def __init__(self, parent, text, title = 'NVDA JSON'):
        super(JsonManipulatorDialog, self).__init__(parent, title = title)
        self.text = text.strip()
        self.load_saved_expressions()
        self.create_ui()
        self.original_text.SetValue(self.text)

    def load_saved_expressions(self):
        if not os.path.exists(SAVED_EXPRESSIONS_FILE_NAME):
            self.saved_expressions = []
        else:
            with open(SAVED_EXPRESSIONS_FILE_NAME, 'r', encoding='utf-8') as file:
                self.saved_expressions = json.load(file)

    def create_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        json_sizer = wx.BoxSizer(wx.VERTICAL)
        label_original_text = wx.StaticText(self, label = 'Original text')
        self.original_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        json_sizer.Add(label_original_text)
        json_sizer.Add(self.original_text, 1, wx.EXPAND | wx.ALL, 5)
        self.label_manipulation_expression = wx.StaticText(self)
        self.manipulation_expression = wx.TextCtrl(self, style=wx.TE_LEFT|wx.TE_PROCESS_ENTER )
        json_sizer.Add(self.label_manipulation_expression)
        json_sizer.Add(self.manipulation_expression, 0, wx.EXPAND | wx.ALL, 5)
        label_output = wx.StaticText(self, label='Output')
        self.output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        json_sizer.Add(label_output)
        json_sizer.Add(self.output, 1, wx.EXPAND | wx.ALL, 5)
        copy_output_button = wx.Button(self, label='Copy output to clipboard')
        copy_output_button.Bind(wx.EVT_BUTTON, self.on_copy_output_click)
        json_sizer.Add(copy_output_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        main_sizer.Add(json_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
        self.manipulation_expression.Bind(wx.EVT_TEXT_ENTER, self.manipulate)
        self.manipulation_expression.Bind(wx.EVT_KEY_DOWN, self.on_manipulation_expression_key_down)

    def on_copy_output_click(self, event):
        copied = api.copyToClip(self.output.GetValue())
        if copied:
            ui.message('Copied')
        else:
            ui.message('Error when copying')

    def on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def on_manipulation_expression_key_down(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_RETURN and event.ControlDown():
            try:
                self.manipulate(event)
            except Exception as e:
                return
            self.save_expression()
        else:
            event.Skip()

    def save_expression(self):
        expression = self.manipulation_expression.GetValue().strip()
        if expression == '':
            ui.message('Empty expression')
            return
        expression_exists = any(
            saved['type'] == self.expression_type and saved['expression'] == expression
            for saved in self.saved_expressions
        )
        if expression_exists:
            ui.message('Query already exists')
            return
        self.saved_expressions.append({
            'type': self.expression_type,
            'expression': expression,
        })
        with open(SAVED_EXPRESSIONS_FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(self.saved_expressions, file, ensure_ascii=False, indent=2)
        ui.message('Query saved')

    def set_output(self, output):
        self.output.SetValue(output if output is not None else '')

    def exit_with_error(self, message):
        wx.CallAfter(
            lambda: gui.messageBox(message, 'Error', wx.OK | wx.ICON_ERROR)
        )
        self.Destroy()

    def parse_text(self, text, multi):
        if multi:
            return self.parse_text_multi(text)
        else:
            return self.parse_text_single(text)

    def parse_text_single(self, text):
        try:
            parsed_json = json.loads(text)
            return self.format_json(parsed_json)
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
        return self.format_json(parsed_jsons_list)

    def format_json(self, data):
        return json.dumps(
            data,
            ensure_ascii = False,
            indent=4,
            sort_keys=True
        )
