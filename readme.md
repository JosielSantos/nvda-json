# NVDA JSON addon

JSON utilities for NVDA.

## Usage

* NVDA+j: If there is text selected, takes the selected JSON text and shows it formatted in a NVDA browseable dialog. If no text is selected, it shows the formatted Json text dialog taking the Json data from the clipboard.
* NVDA+shift+j: formats multiple JSONS in the same text

### How multi JSONS feature works

There are situations that we have multiple JSONs, one per line (log lines for example):

```
{"datetime": "2022-03-10 21:04:05", "level": "info", "message": "user logged in"}
{"datetime": "2022-03-10 21:04:08", "level": "error", "message": "Database is down"}
```

When you press "NVDA+shift+j" this plugin takes each line, formats and displays all elements as a list.
