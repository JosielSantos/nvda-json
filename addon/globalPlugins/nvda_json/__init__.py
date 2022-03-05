import api
import globalPluginHandler
import textInfos
import treeInterceptorHandler
import ui
import json

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def _get_selected_text(self):
        # Code adapted from script_reportCurrentSelection on the NVDA source code

        obj=api.getFocusObject()
        treeInterceptor=obj.treeInterceptor
        if isinstance(treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor) and not treeInterceptor.passThrough:
            obj=treeInterceptor

        try:
            info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info=None

        if not info or info.isCollapsed:
            return ""
        else:
            return info.text

    def script_formatJsonFromSelectedTextOrClipboard(self, gesture):
        selected_text = self._get_selected_text()
        text = selected_text or api.getClipData()

        try:
            parsedJson = json.loads(text)
        except json.decoder.JSONDecodeError as error:
            ui.message('Invalid JSON: %s' % error)

        formattedJson = json.dumps(parsedJson, indent=4, sort_keys=True)
        ui.browseableMessage(formattedJson, 'Formatted JSON', False)

    __gestures = {
        "kb:nvda+j": "formatJsonFromSelectedTextOrClipboard",
    }
