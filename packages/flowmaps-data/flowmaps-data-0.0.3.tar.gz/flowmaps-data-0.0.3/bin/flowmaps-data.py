#!/usr/bin/env python3

import sys
import argparse
import flowmaps_data.settings as settings


usage_str = '''
usage: flowmaps-data.py [-h] COLLECTION [download list list_dates describe]

examples: 

    # Geojson layers
    flowmaps-data.py layers list
    flowmaps-data.py layers describe --layer cnig_provincias --provenance
    flowmaps-data.py layers describe --layer cnig_provincias --plot
    flowmaps-data.py layers download --layer cnig_provincias

    # Consolidated COVID-19 health data
    flowmaps-data.py covid19 list
    flowmaps-data.py covid19 describe --ev ES.covid_cpro
    flowmaps-data.py covid19 download --ev ES.covid_cpro --output_file out.csv --output_type csv

    # Population
    flowmaps-data.py population list
    flowmaps-data.py population describe --layer cnig_provincias
    flowmaps-data.py population download --layer zbs_15 --output_file out.csv

    # Origin-destination daily mobility (from MITMA)
    flowmaps-data.py daily_mobility_matrix list
    flowmaps-data.py daily_mobility_matrix describe
    flowmaps-data.py daily_mobility_matrix download --source_layer cnig_provincias --target_layer cnig_provincias --date 2020-10-10 --output_file out.csv

    # Daily zone movements (from MITMA)
    flowmaps-data.py zone_movements list
    flowmaps-data.py zone_movements describe
    flowmaps-data.py zone_movements download --layer cnig_provincias --output_file out.csv --start-date 2020-10-10 --end-date 2020-10-10

    # Raw datasets
    flowmaps-data.py datasets list
    flowmaps-data.py datasets describe --ev ES.covid_cpro
    flowmaps-data.py datasets download --ev ES.covid_cpro --output_file out.csv --output_type csv
'''

def print_usage():
    print(usage_str)


def execute_command(fn, argparse_spec, commandline):
    parser = argparse.ArgumentParser(description='')
    for arg, options in argparse_spec.items():
        parser.add_argument(arg, **options)
    args = parser.parse_args(commandline)
    fn(**vars(args))


def parse_commandline(config, commandline):
    subcmd = config
    for i, word in enumerate(commandline):
        if word in subcmd:
            subcmd = subcmd[word]
        
        if 'fn' in subcmd:
            # print('calling fn', subcmd['fn'], subcmd['argparse'], commandline[i+1:])
            return execute_command(subcmd['fn'], subcmd['argparse'], commandline[i+1:])
        elif 'subcommands' in subcmd:
            subcmd = subcmd['subcommands']
        else:
            print_usage()
            print(f"Unknown command '{word}'. Available options are: {', '.join(subcmd.keys())}")
            return

    print_usage()
    print(f"Available options are: {', '.join(subcmd.keys())}")


if __name__ == '__main__':
    commandline = sys.argv[1:]
    parse_commandline(settings.CONFIG, commandline)
