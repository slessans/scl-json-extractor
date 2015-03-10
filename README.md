# scl-json-extractor
A command-line utility for extracting keys out of lists of json objects.

```
usage: scl_json_extract.py [-h] [--strict] [--format FORMAT]
                           input_file keys [keys ...]

Extracts arbitrarily nested keys from json array of objects.

positional arguments:
  input_file       the input json file to process
  keys             keys to extract

optional arguments:
  -h, --help       show this help message and exit
  --strict         If specified, objects not containing the specified key path
                   will cause the program to throw an error instead of using a
                   default value.
  --format FORMAT
```

## Inputs
### Input File
The first argument is the path to a json file that should have a root object that is a list of other json objects.

### Keys
A space-separated list of key-paths to extract. A key-path is a list of one or more keys separated by a '.' character. See examples for more clarity.

### Strict
Boolean flag, defaults to false. Default (false) behavior is not-strict: if any keypaths dont exist on a given object, they are ignored and given a default value of `null`. If true, keypaths that don't exist raise an error and program halts execution.

### Format
The --format flag specified the output format. For now this can be one of `json`, `json-pretty` or `csv`. It defaults to `json-pretty`.

## Examples
Assume input_file.json contains the following content:
```json
[
  {
    "type": "sandwich",
    "ingredients": {
      "pork": 1,
      "mayo": 1.4,
      "lettuce": 2,
      "jalapeno": 8
    },
    "yumminess": 10
  },
  {
    "type": "hamburger",
    "ingredients": {
      "ham": 1,
      "burger": 1,
      "jalapeno": 34,
      "cheese": "na"
    },
    "yumminess": "off the charts",
    "health": -2
  }
]
```

### Default Usage
```
./scl_json_extract.py example.json type ingredients.jalepenos yumminess
```

```json
[
  {
    "ingredients.jalapeno": 8,
    "type": "sandwich",
    "yumminess": 10
  },
  {
    "ingredients.jalapeno": 34,
    "type": "hamburger",
    "yumminess": "off the charts"
  }
]
```

### Specify Output Format
```
./scl_json_extract.py --format csv example.json type ingredients.jalapeno yumminess
```

```csv
type,ingredients.jalapeno,yumminess
sandwich,8,10
hamburger,34,off the charts
```

### Default Values
```
./scl_json_extract.py example.json type ingredients.jalapeno ingredients.ham
```

```json
[
  {
    "ingredients.ham": null,
    "ingredients.jalapeno": 8,
    "type": "sandwich"
  },
  {
    "ingredients.ham": 1,
    "ingredients.jalapeno": 34,
    "type": "hamburger"
  }
]
```

### Strict Mode
```
./scl_json_extract.py --strict example.json type ingredients.jalapeno ingredients.ham
```

```
Key 'ingredients.ham' is missing
```

## Coming Soon
Tests, better docs, more complete API, handdling of custom default values.
