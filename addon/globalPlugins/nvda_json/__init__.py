import os
import sys
sys.path.append(os.path.dirname(__file__)+'/../../modules')

import api
import globalPluginHandler
import gui
import textInfos
import treeInterceptorHandler
import ui
import wx

from .json_query_dialog import JsonQueryDialog

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.jsonQueryDialog = None
        self.setupMenu()

    def setupMenu(self):
        self.menu = wx.Menu()
        tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
        for item in self.__features:
            menu_item = self.menu.Append(wx.ID_ANY, item['title'], item['description'])
            item_handler = getattr(self, ('script_' + item['script']))
            gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, item_handler, menu_item)
        self.json_menu = tools_menu.AppendSubMenu(self.menu, "JSON", "NVDA JSON")

    def terminate(self):
        try:
            if self.jsonQueryDialog is not None:
                self.jsonQueryDialog.Destroy()
        except (AttributeError, RuntimeError):
            pass

    def script_format_json_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        self.show_dialog(text, False)

    def script_format_multiple_jsons_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        self.show_dialog(text, True)

    def show_dialog(self, text, multi):
        self.jsonQueryDialog = JsonQueryDialog(gui.mainFrame, text, multi)
        if not self.jsonQueryDialog.IsShown():
            gui.mainFrame.prePopup()
            self.jsonQueryDialog.Show()
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
            'shortcut': 'kb:nvda+j',
            'script': 'format_json_from_selected_text_or_clipboard',
            'title': 'Query and format single JSON entry',
            'description': 'Parse a single JSON entry',
        },
        {
            'shortcut': 'kb:nvda+shift+j',
            'script': 'format_multiple_jsons_from_selected_text_or_clipboard',
            'title': 'Query and format multiple JSON entries',
            'description': 'Parses multiple JSON strings (onne per line)',
        },
    ]
    __gestures = {
        feature['shortcut']: feature['script']
        for feature in __features
        if feature.get('shortcut') is not None
    }
