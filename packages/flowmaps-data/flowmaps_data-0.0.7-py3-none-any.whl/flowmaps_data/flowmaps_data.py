#!/usr/bin/env python3

import sys
import argparse

from . import commands


CONFIG = {
    "layers": {
        "subcommands": {
            "list": {
                "fn": commands.list_layers,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_layer,
                "argparse": {
                    "--layer": {"required": True, "type": str, "help": "", },
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                    "--plot": {"required": False, "default": False, "action": "store_true", "help": "", },
                },
            },
            "download": {
                "fn": commands.download_layer,
                "argparse": {
                    "--layer": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": False, "default": None, "type": str, "help": "", },
                    "--plot": {"required": False, "default": False, "action": "store_true", "help": "", },
                    "--no_save": {"required": False, "default": False, "action": "store_true", "help": "", },
                },
            },
        },
    },
    "covid19": {
        "subcommands": {
            "list": {
                "fn": commands.list_health,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_health,
                "argparse": {
                    "--ev": {"required": True, "type": str, "help": "", },
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                },
            },
            "download": {
                "fn": commands.download_health,
                "argparse": {
                    "--ev": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": True, "type": str, "help": "", },
                    "--output_format": {"required": False, "default": "csv", "type": str, "help": "", },
                    "--start-date": {"dest": "start_date", "required": False, "type": str, "help": "", },
                    "--end-date": {"dest": "end_date", "required": False, "type": str, "help": "", },
                },
            },
        },
    },
    "datasets": {
        "subcommands": {
            "list": {
                "fn": commands.list_data,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_data,
                "argparse": {
                    "--ev": {"required": True, "type": str, "help": "", },
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                },
            },
            "download": {
                "fn": commands.download_data,
                "argparse": {
                    "--ev": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": True, "type": str, "help": "", },
                    "--output_format": {"required": False, "default": "csv", "type": str, "help": "", },
                    "--start-date": {"dest": "start_date", "required": False, "type": str, "help": "", },
                    "--end-date": {"dest": "end_date", "required": False, "type": str, "help": "", },
                },
            },
        },
    },
    "daily_mobility_matrix": {
        "subcommands": {
            "list": {
                "fn": commands.list_daily_mobility_matrix,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_daily_mobility_matrix,
                "argparse": {
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                },
            },
            "download": {
                "fn": commands.download_daily_mobility_matrix,
                "argparse": {
                    "--source_layer": {"required": True, "type": str, "help": "", },
                    "--target_layer": {"required": True, "type": str, "help": "", },
                    "--date": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": True, "type": str, "help": "", },
                    "--output_format": {"required": False, "default": "csv", "type": str, "help": "", },
                },
            },
        },
    },
    "zone_movements": {
        "subcommands": {
            "list": {
                "fn": commands.list_zone_movements,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_zone_movements,
                "argparse": {
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                },
            },
            "download": {
                "fn": commands.download_zone_movements,
                "argparse": {
                    "--layer": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": True, "type": str, "help": "", },
                    "--output_format": {"required": False, "default": "csv", "type": str, "help": "", },
                    "--start-date": {"dest": "start_date", "required": False, "type": str, "help": "", },
                    "--end-date": {"dest": "end_date", "required": False, "type": str, "help": "", },
                },
            },
        },
    },
    "population": {
        "subcommands": {
            "list": {
                "fn": commands.list_population_layers,
                "argparse": {},
            },
            "describe": {
                "fn": commands.describe_population,
                "argparse": {
                    "--layer": {"required": True, "type": str, "help": "", },
                    "--provenance": {"required": False, "default": False, "action": "store_true", "help": "show provenance", },
                },
            },
            "download": {
                "fn": commands.download_population,
                "argparse": {
                    "--layer": {"required": True, "type": str, "help": "", },
                    "--output_file": {"required": True, "type": str, "help": "", },
                    "--output_format": {"required": False, "default": "csv", "type": str, "help": "", },
                    "--start-date": {"dest": "start_date", "required": False, "type": str, "help": "", },
                    "--end-date": {"dest": "end_date", "required": False, "type": str, "help": "", },
                },
            },
        },
    },
}


usage_str = '''
usage: flowmaps-data.py [-h] COLLECTION [list describe download]

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


def main():
    commandline = sys.argv[1:]
    parse_commandline(CONFIG, commandline)


if __name__ == '__main__':
    main()
