import config
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel as BaseSettingsPanel

import wx

class SettingsPanel(BaseSettingsPanel):
    title = 'JSON'

    def makeSettings(self, sizer):
        helper = guiHelper.BoxSizerHelper(self, sizer=sizer)
        json_query_engines = ['jq', 'jsonpath']
        self.radio_box_json_query_engines = wx.RadioBox(self, wx.ID_ANY, 'JSON query Engine', choices = ['JQ', 'JSONPath'], majorDimension = len(json_query_engines), style = wx.RA_SPECIFY_COLS)
        self.radio_box_json_query_engines.SetSelection(json_query_engines.index(config.conf['json']['query_engine']))
        helper.addItem(self.radio_box_json_query_engines)

    def onSave(self):
        config.conf['json']['query_engine'] = self.radio_box_json_query_engines.GetStringSelection().lower()

    def onPanelDeactivated(self):
        self.Show()

    def onPanelDeactivated(self):
        self.Hide()
