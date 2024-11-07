import json
import ui
import wx

class JsonDialog(wx.Dialog):
    def __init__(self, parent, text, multi):
        super(JsonDialog, self).__init__(parent, title="NVDA JSON")
        self.text = text
        self.multi = multi
        self.create_ui()
        self.originalText.SetValue(text)
        self.output.SetValue(self.parse_text(self.text, self.multi))

    def create_ui(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        jsonSizer = wx.BoxSizer(wx.VERTICAL)
        originalTextLabel = wx.StaticText(self, label = "Original text")
        self.originalText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        jsonSizer.Add(originalTextLabel)
        jsonSizer.Add(self.originalText, 1, wx.EXPAND | wx.ALL, 5)
        outputLabel = wx.StaticText(self, label="Output")
        self.output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        jsonSizer.Add(outputLabel)
        jsonSizer.Add(self.output, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(jsonSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

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
        except json.decoder.JSONDecodeError as error:
            ui.message('Invalid JSON: %s' % error)
        return self.__format_json(parsed_json)

    def parse_text_multi(self, text):
        lines = filter(lambda line: line != '', map(lambda line: line.strip(), text.splitlines()))
        parsed_jsons_list = []
        for line in lines:
            try:
                parsed_jsons_list.append(json.loads(line))
            except json.decoder.JSONDecodeError as error:
                continue
        if parsed_jsons_list == []:
            ui.message('No JSONs to display')
        return self.__format_json(parsed_jsons_list)

    def __format_json(self, parsed_json):
        return json.dumps(
            parsed_json,
            indent=4,
            sort_keys=True
        )