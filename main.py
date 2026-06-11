"""CLI entrypoint for the EML parser."""

import argparse
import sys

from parser import parse_eml
from storage import save_email_to_disk


def main():
    """Parse command-line arguments and execute the EML parsing workflow."""

    arg_parser = argparse.ArgumentParser(
        description='A CLI tool for parsing .eml files and extracting '
                    'metadata, content, and attachments.'
    )
    arg_parser.add_argument(
        'eml_file',
        type=str,
        help='.eml file to parse.',
    )
    arg_parser.add_argument(
        'output_dir',
        type=str,
        help='Output directory for the parsed .eml file contents.',
    )

    args = arg_parser.parse_args()

    try:
        print(f'Reading file: {args.eml_file!r}...')
        eml = parse_eml(args.eml_file)

        print(f'Extracting data to directory: {args.output_dir!r}...')
        save_email_to_disk(eml, args.output_dir)

        print(f'{args.eml_file!r} parsed successfully.')
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
