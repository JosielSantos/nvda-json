import api
import globalPluginHandler
import gui
import textInfos
import treeInterceptorHandler
import ui
from .json_dialog import JsonDialog

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.jsonDialog = None

    def terminate(self):
        try:
            if self.jsonDialog is not None:
                self.jsonDialog.Destroy()
        except (AttributeError, RuntimeError):
            pass

    def script_format_json_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        self.show_dialog(text, False)

    def script_format_multiple_jsons_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        self.show_dialog(text, True)

    def show_dialog(self, text, multi):
        self.jsonDialog = JsonDialog(gui.mainFrame, text, multi)
        if not self.jsonDialog.IsShown():
            gui.mainFrame.prePopup()
            self.jsonDialog.Show()
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


    __gestures = {
        'kb:nvda+j': 'format_json_from_selected_text_or_clipboard',
        'kb:nvda+shift+j': 'format_multiple_jsons_from_selected_text_or_clipboard',
    }
