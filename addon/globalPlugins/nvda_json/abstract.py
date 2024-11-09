import json

import gui
import ui

import wx

class Dialog(wx.Dialog):
    def __init__(self, parent, text, title = 'NVDA JSON'):
        super(Dialog, self).__init__(parent, title = title)
        self.text = text
        self.create_ui()

    def onKey(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def onClose(self, evt):
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

    def exit_with_error(self, message):
        wx.CallAfter(
            lambda: gui.messageBox(message, 'Error', wx.OK | wx.ICON_ERROR)
        )
        self.Destroy()

    def format_json(self, parsed_json):
        return json.dumps(
            parsed_json,
            ensure_ascii = False,
            indent=4,
            sort_keys=True
        )
