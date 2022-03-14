import api
import globalPluginHandler
import textInfos
import treeInterceptorHandler
import ui
import json

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_format_json_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        try:
            parsed_json = json.loads(text)
        except json.decoder.JSONDecodeError as error:
            ui.message('Invalid JSON: %s' % error)
        formatted_json = self.__format_json(parsed_json)
        ui.browseableMessage(formatted_json, 'Formatted JSON', False)

    def script_format_multiple_jsons_from_selected_text_or_clipboard(self, gesture):
        text = self.__get_text()
        lines = filter(lambda line: line != '', map(lambda line: line.strip(), text.splitlines()))
        parsed_jsons_list = []
        for line in lines:
            try:
                parsed_jsons_list.append(json.loads(line))
            except json.decoder.JSONDecodeError as error:
                continue
        if parsed_jsons_list == []:
            ui.message('No JSONs to display')
        formatted_json = self.__format_json(parsed_jsons_list)
        ui.browseableMessage(formatted_json, 'Formatted JSONs', False)

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

    def __format_json(self, parsed_json):
        return json.dumps(parsed_json, indent=4, sort_keys=True)


    __gestures = {
        'kb:nvda+j': 'format_json_from_selected_text_or_clipboard',
        'kb:nvda+shift+j': 'format_multiple_jsons_from_selected_text_or_clipboard',
    }
