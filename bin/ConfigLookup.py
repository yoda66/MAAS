#!/usr/bin/env python3

import sys
import yaml
import argparse


class ConfigLookup():

    def __init__(self, configfile, text, pk=False, pv=True):
        self.configfile = configfile
        self.text = text.split('.')
        self.pk = pk
        self.pv = pv
        result = self.lookup()
        if pv and result is not None:
            print(result)

    def lookup(self):
        with open(self.configfile, 'rt') as f:
            self.config = yaml.load(f, Loader=yaml.Loader)
        if self.text[0] not in self.config:
            print('[*] Cannot locate configuration item {}'.format(self.text))
            return
        return self.search_config(self.config)

    def search_config(self, config, i=0):
        try:
            k = self.text[i]
        except Exception:
            return config

        if k in config and isinstance(config[k], dict) and i < len(self.text):
            return self.search_config(config[k], i+1)

        if k in config and k == self.text[-1]:
            if self.pk:
                print(f'{k}: ', end='')
            return config[k]
        print('[*] Cannot locate configuration item {}'.format('.'.join(self.text)))
        return


if __name__ == '__main__':
    banner = '''
___________________________________________

   ConfigLookup.py
   Version 1.1
   Author: Joff Thyer (c) 2023
   Black Hills Information Security LLC
___________________________________________

'''
    sys.stderr.write(banner)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', default='config.yml', help='YML configuration file'
    )
    parser.add_argument(
        '-pk', '--printkey', default=False, action='store_true',
        help='Also print the key upon lookup'
    )
    parser.add_argument('text', help='text arg to lookup')
    args = parser.parse_args()
    ConfigLookup(args.c, args.text, args.printkey)
