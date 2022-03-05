# -*- coding: UTF-8 -*-

import os.path

def _(arg):
        return arg


addon_info = {
        "addon_name": "nvda-json",
        "addon_summary": _("NVDA JSON"),
        "addon_description": _("""JSON utilities for NVDA
"""),
        "addon_version": "0.3",
        "addon_author": "Josiel Santos <josiel.lkp@gmail.com>",
        "addon_url": "https://github.com/JosielSantos/nvda-json",
        "addon_docFileName": "readme.html",
        "addon_minimumNVDAVersion": "2019.3.0",
        "addon_lastTestedNVDAVersion": "2021.1",
        "addon_updateChannel": None,
}

pythonSources = [os.path.join("addon", "globalPlugins", "nvda-json", "*.py")]
i18nSources = pythonSources + ["buildVars.py"]
excludedFiles = []
baseLanguage = "en"
markdownExtensions = []
