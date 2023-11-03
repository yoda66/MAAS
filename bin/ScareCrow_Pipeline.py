#!/usr/bin/env python3

import os
import pathlib
import argparse
import sys
from ConfigLookup import ConfigLookup


class GenerateConfig():

    def __init__(self, stage, tag, configfile):
        self.stage = stage
        self.tag = tag
        o = ConfigLookup(configfile, 'ScareCrow', pv=False).lookup()
        self.print_config(o)

    def print_config(self, o, enable=True):
        config = f'''
stages:
    - {self.stage}
'''

        extras = ''
        if 'injection' in o and o['injection']:
            extras += f" -injection {o['injection']}"

        # payload signing
        if 'valid' in o and 'password' in o:
            extras += f" -valid {o['valid']} -password {o['password']}"
        elif 'domain' in o:
            extras += f" -domain {o['domain']}"
        else:
            extras += f" -nosign"

        # payload delivery option
        delivery = ['']
        if 'delivery' in o and 'url' in o:
            extras += f" -url {o['url']}"
            delivery = o['delivery']

        # boolean flags
        for k in o:
            v = o[k]
            if isinstance(v, bool) and k != 'enable' and v:
                extras += f' -{k}'

        for i, loader in enumerate(o['loader']):
            if not (loader == 'binary' or loader == 'dll') and '-O' not in extras:
                extras += f' -O output.js'

            for dm in delivery:
                outdir_postfix = ''
                if dm and not (loader == 'binary' or loader == 'dll'):
                    extras += f' -delivery {dm}'
                    outdir_postfix = f'-{dm}'

                config += f'''
ScareCrow{i:02d}:
    stage: {self.stage}
    tags:
        - {self.tag}
    script:
        - |
            cd /payloads/${{CI_COMMIT_SHORT_SHA}}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader {loader}{extras}

'''
        print(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', default='Config.yml',
        help='YAML configuration file'
    )
    parser.add_argument(
        '-s', '--stage', default='ScareCrow',
        help='build stage'
    )
    parser.add_argument(
        '-t', '--tag', default='maas',
        help='job tag'
    )
    args = parser.parse_args()
    GenerateConfig(args.stage, args.tag, args.c)
