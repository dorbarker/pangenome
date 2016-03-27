#!/usr/bin/env python3

import argparse
from getpass import getuser
import os
import subprocess
import sys

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--fasta-dir', required = True,
                        help = 'Path to fasta directory to be analyzed.')

    parser.add_argument('--work-dir', help = 'Path to work directory \
                                      (default = one level up from fasta-dir)')

    return parser.parse_args()

def find_panseq():
    '''Tries first to find panseq with coreutils find'''

    p = subprocess.Popen(['find', os.path.expanduser('~'),
                          '-name', '*lib/panseq.pl'],
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)

    out, err = p.communicate()

    if out == '':
        sys.stderr.write('Could not locate panseq.pl\n')
        sys.exit(1)
    else:
        return out

