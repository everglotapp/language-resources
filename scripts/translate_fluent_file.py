from fluent.syntax import parse, ast, serialize
from fluent.syntax.ast import from_json
import os
import requests
import argparse
import json
from pathlib import Path, PurePath

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str,
                    help="Path to locale folder",
                    required=True)
parser.add_argument("--filename", type=str,
                    help="filename of which to be translated in en locale",
                    required=True)
parser.add_argument("--locale", type=str,
                    help="Locale to be translated into",
                    required=True)
parser.add_argument("--apikey", type=str,
                    help="Deepl API key",
                    required=True)
args = parser.parse_args()

def deepl_translate(sentence, target_lang):
    response = requests.post(url='https://api-free.deepl.com/v2/translate',
                          data = {
                            'target_lang' : target_lang,  
                            'auth_key' : args.apikey,
                            'text': sentence
                          })
    r = json.loads(response.text)
    translated = r['translations'][0]['text']
    return translated

def translate_element(resource_dict):
    for element in resource_dict['body']:
        if element['type'] != 'Message':
            continue
        else:
            for subelement in element['value']['elements']:
                if subelement['type'] == 'TextElement':
                    subelement['value'] = deepl_translate(subelement['value'], args.locale.upper())
                    print(subelement['value'])
                else:
                    continue
    return resource_dict

if __name__ == "__main__":
    Path(args.path + args.locale.lower()).mkdir(parents=True, exist_ok=True)
    with open(PurePath(args.path, 'en', args.filename), 'r') as file:
        data = file.read()
    resource = parse(data)
    resource_dict = resource.to_json()
    resource_dict = translate_element(resource_dict)
    ast = from_json(resource_dict)
    with open(PurePath(args.path, args.locale, args.filename), 'w') as file:
        file.write(serialize(ast))
