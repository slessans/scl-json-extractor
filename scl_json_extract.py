#! /usr/bin/env python3

import json
import csv
import argparse
import sys


def _is_valid_leaf(val):
    return val is None or isinstance(val, (int, str, float, bool))


class NonExistentKeyException(Exception):
    def __init__(self, key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key


class KeyExtractor(object):

    def __init__(self, key: str, strict=False, default=None):
        self.key = key
        self._key_path = self.key.split('.')
        self.strict = strict
        self.default = default

    def __call__(self, obj: dict):
        val = obj

        for k in self._key_path:
            if isinstance(val, dict) and k in val:
                val = val[k]
            elif self.strict:
                raise NonExistentKeyException(self.key)
            else:
                return self.default

        return val


def _extract_from_object(extractors, obj: dict):
    assert isinstance(obj, dict)
    if not extractors:
        return obj
    return {extractor.key: extractor(obj) for extractor in extractors}


def _main():
    parser = argparse.ArgumentParser(
        description='Extracts arbitrarily nested keys from json array of objects.'
    )
    
    parser.add_argument('input_file', type=str, help='the input json file to process')
    parser.add_argument('keys', type=str, nargs='+', help='keys to extract')
    parser.add_argument('--strict', action='store_const', const=True, default=False,
                        help='If specified, objects not containing the specified key path will cause '
                             'the program to throw an error instead of using a default value.')

    parser.add_argument('--format', type=str, default='json-pretty')

    args = parser.parse_args()
    extractors = list(KeyExtractor(k, strict=args.strict) for k in args.keys)

    with open(args.input_file) as in_file:
        in_data = json.load(in_file)

    assert isinstance(in_data, list)

    try:
        out = list(_extract_from_object(extractors, d) for d in in_data)
    except NonExistentKeyException as e:
        print("Key '%s' is missing" % (e.key,), file=sys.stderr)  # TODO more descriptive error handling (where in file?, etc)
        return 1

    if args.format == 'json' or args.format == 'json-pretty':
        if args.format == 'json-pretty':
            json_args = {
                'sort_keys': True,
                'indent': 2,
                'separators': (',', ': '),
            }
        else:
            json_args = {}

        print(json.dumps(out, **json_args))

    elif args.format == 'csv':
        writer = csv.DictWriter(sys.stdout, fieldnames=list(e.key for e in extractors))
        writer.writeheader()
        writer.writerows(out)

    else:
        print('output format %s is not valid' % (args.format,), file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    exit(_main())
