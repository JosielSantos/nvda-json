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

### JSONPath

Between the "original text" and the "output" is a "path expression" field.
This field accepts a JSONPath expression.
JSONPath is a syntax that allows filtering JSON items. You can write the
expression and press enter to see the filtered result in the "output" field.

You can learn JSONPath in the [documentation](https://goessner.net/articles/JsonPath/)

Let's discover this feature by example.

Given these JSON lines:

```
{"name": "Josiel", "gender": "male", "birth_date": "1995-07-03"}
{"name": "Luzia", "gender": "female", "birth_date": "1945-03-19"}
{"name": "PH", "gender": "male", "birth_date": "2004-03-18"}
```

#### Get all people names

```
$..name
```

#### Get only male people

```
$[?(@.gender == 'male')]
```

#### Get only young people (born before year 2000)

```
$[?(@.birth_date > '2000-01-01')]
```

#### Get the original JSON

```
$
```

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

## Features (implemented and future)

* [x] Parsing JSON from clipboard
* [x] Parsing JSON from selected text (cursor)
* [x] Parsing of multiple JSON strings (one per line)
* [ ] Settings panel
  * [ ] Configure scripts behaviour (take JSON only from selected text, only from clipboard or both (current))
* [ ] Parsing JSON variants
  * [x] Original JSON using Python's json module
  * [ ] json5
* [ ] Interactive JSON through a UI
  * [x] Button to copy output to clipboard
  * [ ] JSON Filtering / transformation
    * [x] With JSONPath (https://goessner.net/articles/JsonPath/, https://github.com/h2non/jsonpath-ng)
    * [ ] With JQ (https://jqlang.github.io/jq/, https://github.com/mwilliamson/jq.py)
    * [ ] Save filters / transformations to avoid typing (program and description)
    * [x] String transformation using JSONPointer (https://datatracker.ietf.org/doc/html/rfc6901, https://github.com/stefankoegl/python-json-pointer?tab=readme-ov-file)
