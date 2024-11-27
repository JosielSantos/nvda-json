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

The formatted text will be displaied as follows:

```
[
    {
        "datetime": "2022-03-10 21:04:05",
        "level": "info",
        "message": "user logged in"
    },
    {
        "datetime": "2022-03-10 21:04:08",
        "level": "error",
        "message": "Database is down"
    }
]
```

### JSON Filtering / Transformation

This addon allows you to filter / transform JSON using JQ or JSONPath.
By default JQ is used, but you can change this in the settings panel of NVDA.

When you open the JSON dialog using "NVDA+j" or "NVDA+shift+j" you can see three text boxes: original text, query expression and output.
You must use the second text field to filter / transform JSON. You type the query, press enter and check the result in the "output" text field.

To test this feature you can use this fake log file:

```
{"timestamp": "2024-11-07T14:12:45Z", "level": "INFO", "trace_id": "abc123", "span_id": "span789", "message": "User login successful"}
{"timestamp": "2024-11-07T14:13:12Z", "level": "ERROR", "trace_id": "def456", "span_id": "span101", "message": "Failed to connect to database"}
{"timestamp": "2024-11-07T14:15:30Z", "level": "DEBUG", "trace_id": "ghi789", "span_id": "span202", "message": "Fetching data from cache"}
{"timestamp": "2024-11-07T14:17:02Z", "level": "WARN", "trace_id": "jkl012", "span_id": "span303", "message": "High memory usage detected"}
{"timestamp": "2024-11-07T14:19:25Z", "level": "INFO", "trace_id": "mno345", "span_id": "span404", "message": "Background job started"}
{"timestamp": "2024-11-07T14:21:58Z", "level": "ERROR", "trace_id": "pqr678", "span_id": "span505", "message": "Timeout while waiting for external API response"}
{"timestamp": "2024-11-07T14:23:47Z", "level": "DEBUG", "trace_id": "stu901", "span_id": "span606", "message": "User profile data parsed successfully"}
{"timestamp": "2024-11-07T14:25:15Z", "level": "WARN", "trace_id": "vwx234", "span_id": "span707", "message": "Deprecated API version called"}
{"timestamp": "2024-11-07T14:27:33Z", "level": "INFO", "trace_id": "yzb567", "span_id": "span808", "message": "File uploaded successfully"}
{"timestamp": "2024-11-07T14:29:09Z", "level": "ERROR", "trace_id": "cde890", "span_id": "span909", "message": "Null pointer exception encountered"}
```

#### JQ

JQ is like a programming language to filter and transform JSON data.
Because of this flexibility, this is the default query engine used in this addon.

Example JQ programs:

| description | query |
| ----- | ----- |
| GET the original JSON | `.` |
| Extract all log messages | `.[].message` |
| Get all INFO records | `.[] \| select(.level == "INFO")` |
| Get an object containing only "timestamp" and "message" for WARN records | `.[] \| select(.level == "WARN") \| {timestamp, message}` |
| Get timestamp of records that contains "cache" in the message | `.[] \| select(.message \| test("cache")) \| .timestamp` |
| Get only "message" and "timestamp" field, grouped by level | `group_by(.level) \| map({(.[0].level): map({message: .message, timestamp: .timestamp})})` |
| Get the first three records with DEBUG level | `.[] \| select(.level == "DEBUG") \| . \| limit(3;.)` |
| Add a "is_critical=true" field to ERROR levels and false to others | `.[] \| .is_critical = (.level == "ERROR") \| .` |
| Delete DEBUG records | `map(select(.level != "DEBUG"))` |
| Sort records by timestamp, ascending | `sort_by(.timestamp)` |

#### JSONPath

JSONPath is a syntax that allows filtering JSON items.
You can learn it in the [documentation](https://goessner.net/articles/JsonPath/)

Example queries:

| description | query |
| ----- | ----- |
| Get the original JSON | `$` |
| Extract all log messages | `$..message` |
| Get records with level = ERROR | `$[?(@.level == 'ERROR')]` |
| Extract the field "trace_id" of all INFO records | `$[?(@.level == 'INFO')].trace_id` |
| Get all non-debug records | `$[?(@.level != 'DEBUG')]` |
| Extract all logs before a timestamp | `$[?(@.timestamp > '2024-11-07T14:20:00Z')]` |

### String transformation with JSONPointer (NVDA+ctrl+j)

Original idea from @thgcode in [this issue](https://github.com/JosielSantos/nvda-json/issues/6)

Given this JSON:

```
{
    "name": "Josiel",
    "family": {
        "mother": {"name": "Maria"}
    },
    "programming_languages": ["Java", "PHP"]
}
```

With this functionality you can create strings using placeholders with JSONPointer syntax:

```
My name is {/name}, My mother is {/family/mother/name} and my favorite programming language is {/programming_languages/1}
```

Output:

```
My name is Josiel, My mother is Maria and my favorite programming language is PHP
```

### Using autocomplete

On expression edit field:

* Press ctrl+enter to execute / save a query
* Type part of expression
* Use up / down arrow to access the suggestions list

In the suggestions list:

* Press enter to fill the edit field with the complete expression and execute it
* Press backspace to delete the last character in the edit field and move focus back to it
* Press delete to remove the saved expression

## Features (implemented and future)

* [x] Parsing JSON from clipboard
* [x] Parsing JSON from selected text (cursor)
* [x] Parsing of multiple JSON strings (one per line)
* [ ] Settings panel
  * [x] Option to select the query engine to use
  * [ ] Configure scripts behavior (take JSON only from selected text, only from clipboard or both (current))
* [ ] Parsing JSON variants
  * [x] Original JSON using Python's json module
  * [ ] json5
* [ ] Interactive JSON through a UI
  * [x] Button to copy output to clipboard
  * [x ] JSON Filtering / transformation
    * [x] With JSONPath (https://goessner.net/articles/JsonPath/, https://github.com/h2non/jsonpath-ng)
    * [x] With JQ (https://jqlang.github.io/jq/, https://github.com/mwilliamson/jq.py)
    * [x] Save filters / transformations to avoid typing (program and description)
    * [x] Autocomplete with saved queries
    * [x] String transformation using JSONPointer (https://datatracker.ietf.org/doc/html/rfc6901, https://github.com/stefankoegl/python-json-pointer?tab=readme-ov-file)
