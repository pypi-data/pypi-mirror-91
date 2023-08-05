#!/usr/bin/env python
# coding=utf8
## Copyright (c) 2020 Arseniy Kuznetsov
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

import sys
import subprocess
import pkg_resources
import mktxp.cli.checks.chk_pv
from mktxp.utils.utils import run_cmd
from mktxp.cli.options import MKTXPOptionsParser, MKTXPCommands
from mktxp.cli.config.config import config_handler, ConfigEntry
from mktxp.basep import MKTXPProcessor

class MKTXPDispatcher:
    ''' Base MKTXP Commands Dispatcher
    '''
    def __init__(self):
        self.option_parser = MKTXPOptionsParser()

    # Dispatcher
    def dispatch(self):
        args = self.option_parser.parse_options()

        if args['sub_cmd'] == MKTXPCommands.VERSION:
            self.print_version()

        elif args['sub_cmd'] == MKTXPCommands.INFO:
            self.print_info()

        elif args['sub_cmd'] == MKTXPCommands.SHOW:
            self.show_entries(args)

        elif args['sub_cmd'] == MKTXPCommands.ADD:
            self.add_entry(args)

        elif args['sub_cmd'] == MKTXPCommands.EDIT:
            self.edit_entry(args)

        elif args['sub_cmd'] == MKTXPCommands.DELETE:
            self.delete_entry(args)

        elif args['sub_cmd'] == MKTXPCommands.START:
            self.start_export(args)

        else:
            # nothing to dispatch
            return False

        return True

    # Dispatched methods
    def print_version(self):
        ''' Prints MKTXP version info
        '''
        version = pkg_resources.require("mktxp")[0].version
        print(f'Mikrotik RouterOS Prometheus Exporter version {version}')

    def print_info(self):
        ''' Prints MKTXP general info
        '''
        print(f'{self.option_parser.script_name}: {self.option_parser.description}')


    def show_entries(self, args):
        if args['config']:
            print(f'MKTXP data config: {config_handler.usr_conf_data_path}')
            print(f'MKTXP internal config: {config_handler.mktxp_conf_path}')

        else:
            for entryname in config_handler.registered_entries():
                if args['entry_name'] and entryname != args['entry_name']:
                    continue
                entry = config_handler.entry(entryname)
                print(f'[{entryname}]')
                divider_fields = set(['username', 'use_ssl', 'dhcp'])
                for field in entry._fields:
                    if field == 'password':
                        print(f'    {field}: {"*" * len(entry.password)}')
                    else:
                        if field in divider_fields:
                            print()
                        print(f'    {field}: {getattr(entry, field)}')
                print('\n')

    def add_entry(self, args):
        entry_args = {key: value for key, value in args.items() if key not in set(['sub_cmd', 'entry_name'])}
        config_handler.register_entry(entry_name = args['entry_name'], entry_args = entry_args)

    def edit_entry(self, args):        
        editor = args['editor']
        if not editor:
            print(f'No editor to edit the following file with: {config_handler.usr_conf_data_path}')
        subprocess.check_call([editor, config_handler.usr_conf_data_path])

    def delete_entry(self, args):
        config_handler.unregister_entry(entry_name = args['entry_name'])
        
    def start_export(self, args):
        MKTXPProcessor.start()


def main():
    MKTXPDispatcher().dispatch()

if __name__ == '__main__':
    main()

