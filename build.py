#!/usr/bin/env python

import argparse
import os
import subprocess

from distutils.dir_util import copy_tree
from shutil import copytree

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
TRANSLATOR_DIR = os.path.join(PROJECT_ROOT, 'src', 'translator')

SEARCH_DIR = os.path.join(PROJECT_ROOT, 'src', 'search')

def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Build Power Lifted planner.')
    parser.add_argument('-d', '--debug',
                        action="store_true", help="Build in debug mode.")
    return parser.parse_args()

def get_build_dir(debug):
    if debug:
        return os.path.join(PROJECT_ROOT, 'builds', 'debug')
    else:
        return os.path.join(PROJECT_ROOT, 'builds', 'release')


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def build(debug_flag):
    BUILD_DIR = get_build_dir(debug_flag)
    BUILD_SEARCH_DIR = os.path.join(BUILD_DIR, 'search')
    if debug_flag:
        BUILD_TYPE = 'Debug'
    else:
        BUILD_TYPE = 'Release'
    create_dir(BUILD_DIR)
    create_dir(BUILD_SEARCH_DIR)
    copy_tree(TRANSLATOR_DIR, BUILD_DIR + '/translator')
    subprocess.check_call(['cmake', SEARCH_DIR, '-DCMAKE_OSX_ARCHITECTURES=arm64','-DCMAKE_BUILD_TYPE='+BUILD_TYPE],
                          cwd=BUILD_SEARCH_DIR)
    subprocess.check_call(['make', '-j5'], cwd=BUILD_SEARCH_DIR)


if __name__ == '__main__':
    args = parse_arguments()
    build(args.debug)
