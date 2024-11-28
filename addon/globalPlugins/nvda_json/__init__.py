import os
import sys

import api
import config
import globalPluginHandler
import gui
import textInfos
import treeInterceptorHandler
import wx
from gui.settingsDialogs import NVDASettingsDialog

from .settings_panel import SettingsPanel

conf_spec = {
    'query_engine': 'string(default=jq)',
}
config.conf.spec['json'] = conf_spec


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        sys.path.append(os.path.dirname(__file__) + '/../../modules')
        self.dialogs = []
        self.create_features_menu()
        NVDASettingsDialog.categoryClasses.append(SettingsPanel)

    def create_features_menu(self):
        self.menu = wx.Menu()
        tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
        for item in self.__features:
            menu_item = self.menu.Append(
                wx.ID_ANY, item['title'], item['description'])
            item_handler = getattr(self, ('script_' + item['script']))
            gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, item_handler, menu_item)
        self.json_menu = tools_menu.AppendSubMenu(self.menu, 'JSON', 'NVDA JSON')

    def terminate(self):
        for dialog in self.dialogs:
            self.destroy_dialog(dialog)

    def destroy_dialog(self, dialog):
        try:
            if dialog is not None:
                dialog.Destroy()
        except (AttributeError, RuntimeError):
            pass

    def script_format_json_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        from .json_query_dialog import JsonQueryDialog
        self.show_dialog(JsonQueryDialog(gui.mainFrame, text, False))

    def script_format_multiple_jsons_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        from .json_query_dialog import JsonQueryDialog
        self.show_dialog(JsonQueryDialog(gui.mainFrame, text, True))

    def script_json_template(self, gesture):
        from .json_template_dialog import JsonTemplateDialog
        text = self.__get_text()
        self.show_dialog(JsonTemplateDialog(gui.mainFrame, text))

    def show_dialog(self, dialog):
        self.dialogs.append(dialog)
        if not dialog.IsShown():
            gui.mainFrame.prePopup()
            dialog.Show()
            gui.mainFrame.postPopup()

    def __get_text(self):
        return self.__get_selected_text() or api.getClipData()

    def __get_selected_text(self):
        # Code adapted from script_reportCurrentSelection on the NVDA source code
        focused_object = api.getFocusObject()
        treeInterceptor = focused_object.treeInterceptor
        if isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor) and not treeInterceptor.passThrough:
            focused_object = treeInterceptor
        try:
            info = focused_object.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info = None
        if not info or info.isCollapsed:
            return ''
        else:
            return info.text

    __features = [
        {
            'title': 'Query and format single JSON entry',
            'description': 'Parse a single JSON entry',
            'shortcut': 'kb:nvda+j',
            'script': 'format_json_from_selected_text_or_clipboard',
        },
        {
            'title': 'Query and format multiple JSON entries',
            'description': 'Parses multiple JSON strings (onne per line)',
            'shortcut': 'kb:nvda+shift+j',
            'script': 'format_multiple_jsons_from_selected_text_or_clipboard',
        },
        {
            'title': 'String transformation with JSONPointer',
            'description': 'Create strings using JSONPointer syntax',
            'shortcut': 'kb:nvda+control+j',
            'script': 'json_template',
        },
    ]
    __gestures = {
        feature['shortcut']: feature['script']
        for feature in __features
        if feature.get('shortcut') is not None
    }
