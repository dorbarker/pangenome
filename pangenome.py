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
        sys.stderr.write('FATAL: Could not locate panseq.pl\n')
        sys.exit(1)
    else:
        return out

def find_requirements():

    def which(name, parent_dir = True):
        
        try:
            result = subprocess.check_output(['which', name]).strip()

            return os.path.dirname(result) + '/' if parent_dir else result
        
        except subprocess.CalledProcessError:

            sys.stderr.write('FATAL: Cannot locate {} in PATH\n'.format(name))
            sys.exit(1)

    _args = (('blastn',), ('mummer',), ('muscle', False))
    
    return {args[0]: which(*args) for args in _args}

