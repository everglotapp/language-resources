from jinja2 import Template
from pathlib import Path, PurePath
from utils import unix_time_millis
from datetime import datetime
from constants import LOCALES, COUNTRIES, LOCALES_FULL, TEMPLATE_TYPE
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--outputfolder", type=str,
                    help="Path to migration folder",
                    required=True)
parser.add_argument("--locale", type=str,
                    help="Locale for which to generate migration files",
                    )
parser.add_argument("--template", type=str,
                    help="random-questions, would-you-rather-questions or words. Generate for all if not given."
                    )
args = parser.parse_args()

def generate_migration(locale, template_type, output_folder):
    with open(f"./migration_templates/{template_type}.js", 'r') as file:
        data = file.read()
    tm = Template(data)
    output = tm.render(locale=locale, locale_full=LOCALES_FULL[locale], country=COUNTRIES[locale])
    timestamp = unix_time_millis()
    filename = f'{timestamp}_{template_type}-{locale}.js'
    path = PurePath(output_folder, filename)
    with open(path, 'w') as file:
        file.write(output)


if __name__ == "__main__":
    if args.locale:
        if args.template:
            generate_migration(args.locale, args.template, args.outputfolder)
        else:
            for template in TEMPLATE_TYPE:
                generate_migration(args.locale, template, args.outputfolder)
    else:
        for locale in LOCALES:
            if args.template:
                generate_migration(locale, args.template, args.outputfolder)
            else:
                for template in TEMPLATE_TYPE:
                    generate_migration(locale, template, args.outputfolder)
