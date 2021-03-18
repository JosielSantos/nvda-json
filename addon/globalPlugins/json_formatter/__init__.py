import api
import globalPluginHandler
import ui
import json

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_formatJsonFromClipboard(self, gesture):
        text = api.getClipData()

        try:
            parsedJson = json.loads(text)
        except json.decoder.JSONDecodeError:
            ui.message('Invalid JSON')

        formattedJson = json.dumps(parsedJson, indent=4, sort_keys=True)
        ui.browseableMessage(formattedJson, 'Formatted JSON', False)

    __gestures = {
        "kb:nvda+j": "formatJsonFromClipboard",
    }
