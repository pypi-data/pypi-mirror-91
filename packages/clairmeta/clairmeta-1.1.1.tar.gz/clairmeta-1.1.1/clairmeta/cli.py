#!/usr/bin/env python3
# Clairmeta - (C) YMAGIS S.A.
# See LICENSE for more information

from __future__ import print_function

import os
import argparse
import sys
import json
import dicttoxml
import pprint

from clairmeta import DCP, Sequence
from clairmeta.logger import disable_log
from clairmeta.info import __version__
from clairmeta.profile import load_profile, DCP_CHECK_PROFILE
from clairmeta.settings import SEQUENCE_SETTINGS
from clairmeta.utils.xml import prettyprint_xml
from clairmeta.utils.file import ConsoleProgress


package_type_map = {
    'dcp': DCP,
    'dcdm': Sequence,
    'dsm': Sequence,
    'scan': Sequence,
}

package_check_settings = {
    'dcdm': SEQUENCE_SETTINGS['DCDM'],
    'dsm': SEQUENCE_SETTINGS['DSM'],
    'scan': SEQUENCE_SETTINGS['SCAN'],
}


def cli_check(args):
    try:
        if args.type == 'dcp':
            check_profile = DCP_CHECK_PROFILE
            callback = None

            if args.profile:
                path = os.path.abspath(args.profile)
                check_profile = load_profile(path)
            if args.log:
                check_profile['log_level'] = args.log
            if args.progress:
                callback = ConsoleProgress()
            if args.format != 'text':
                disable_log()

            status, report = DCP(args.path, kdm=args.kdm, pkey=args.key).check(
                profile=check_profile, ov_path=args.ov, hash_callback=callback)

            if args.format == "dict":
                msg = pprint.pformat(report.to_dict())
            elif args.format == "json":
                msg = json.dumps(
                    report.to_dict(), sort_keys=True, indent=2,
                    separators=(',', ': '))
            elif args.format == "xml":
                xml_str = dicttoxml.dicttoxml(
                    report.to_dict(), custom_root='ClairmetaCheck',
                    ids=False, attr_type=False)
                msg = prettyprint_xml(xml_str)

            if args.format != 'text':
                return True, msg

        else:
            obj_type = package_type_map[args.type]
            setting = package_check_settings[args.type]
            status = obj_type(args.path).check(setting)

    except Exception as e:
        status = False
        print("Error : {}".format(e))

    msg = "{} - {} - Check {}".format(
        args.type.upper(), args.path, "succeeded" if status else "failed")
    return status, msg


def cli_probe(args):
    try:
        disable_log()
        kwargs = {}

        if args.type == 'dcp':
            kwargs['kdm'] = args.kdm
            kwargs['pkey'] = args.key

        obj_type = package_type_map[args.type]
        res = obj_type(args.path, **kwargs).parse()

        if args.format == "dict":
            msg = pprint.pformat(res)
        elif args.format == "json":
            msg = json.dumps(
                res, sort_keys=True, indent=2, separators=(',', ': '))
        elif args.format == "xml":
            xml_str = dicttoxml.dicttoxml(
                res, custom_root='ClairmetaProbe', ids=False, attr_type=False)
            msg = prettyprint_xml(xml_str)

        return True, msg
    except Exception as e:
        return False, "Error : {}".format(e)


def get_parser():
    global_parser = argparse.ArgumentParser(
        description='Clairmeta Command Line Interface {}'
        .format(__version__))
    subparsers = global_parser.add_subparsers()

    # DCP
    parser = subparsers.add_parser(
        'check', help="Package validation")
    parser.add_argument('path', help="absolute package path")
    parser.add_argument('-log', default=None, help="logging level [dcp]")
    parser.add_argument('-profile', default=None, help="json profile [dcp]")
    parser.add_argument('-kdm', default=None,
        help="kdm with encrypted keys [dcp]")
    parser.add_argument('-key', default=None,
        help="recipient private key [dcp]")
    parser.add_argument(
        '-format', default="text", choices=['text', 'dict', 'xml', 'json'],
        help="output format [dcp]")
    parser.add_argument(
        '-progress', action='store_true', help="hash progress bar [dcp]")
    parser.add_argument('-ov', default=None, help="ov package path [dcp]")
    parser.add_argument(
        '-type', choices=package_type_map.keys(),
        required=True, help="package type")
    parser.set_defaults(func=cli_check)

    parser = subparsers.add_parser('probe', help="Package metadata extraction")
    parser.add_argument('path', help="absolute package path")
    parser.add_argument('-kdm', default=None, help="kdm with encrypted keys")
    parser.add_argument('-key', default=None, help="recipient private key")
    parser.add_argument(
        '-format', default="dict", choices=['dict', 'xml', 'json'],
        help="output format")
    parser.add_argument(
        '-type', choices=package_type_map.keys(),
        required=True, help="package type")
    parser.set_defaults(func=cli_probe)

    return global_parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        status, msg = args.func(args)
        print(msg)
        sys.exit(0 if status else 1)
