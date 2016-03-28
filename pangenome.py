#!/usr/bin/env python3

import argparse
import csv
from multiprocessing import cpu_count
import os
import subprocess
import sys

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--fasta-dir', required = True,
                        help = 'Path to fasta directory to be analyzed.')

    parser.add_argument('--work-dir', help = 'Path to work directory \
                                      (default = one level up from fasta-dir)')

    parser.add_argument('--word-size', type = int, default = 20,
                        help = 'Word size for BLASTN (default = 20)')

    parser.add_argument('--fragment-size', type = int, default = 500,
                      help = 'Fragment size for Panseq marker classification')
    
    parser.add_argument('--percent-id', type = int, default = 85,
                      help = 'Cutoff for nucleotide level homology')

    parser.add_argument('--cores', type = int, default = cpu_count(),
                        help = 'Number of CPU cores to use')
    
    

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
    '''Locates blastn, mummer, and muscle'''

    def which(name, parent_dir = True):
 
        try:
            result = subprocess.check_output(['which', name]).strip()

            return os.path.dirname(result) + '/' if parent_dir else result

        except subprocess.CalledProcessError:

            sys.stderr.write('FATAL: Cannot locate {} in PATH\n'.format(name))
            sys.exit(1)

    _args = (('blastn',), ('mummer',), ('muscle', False))

    return {args[0]: which(*args) for args in _args}

def format_settings(fasta_dir, work_dir, size, perc_id, word, cores):
    '''Perpares the settings file panseq takes as its only argument'''

    num_strains = sum(1 for x in os.listdir(fasta_dir) if '.f' in x)
    base_dir = os.path.join(work_dir, 'panseq_output/')

    reqs = find_requirements()

    settings = (
        ('queryDirectory',         fasta_dir),
        ('baseDirectory',          base_dir),
        ('numberOfCores',          cores),
        ('mummerDirectory',        reqs['mummer']),
        ('blastDirectory',         reqs['blastn']),
        ('muscleExecutable',       reqs['muscle']),
        ('novelRegionFinderMode',  'no_duplicates'),
        ('minimumNovelRegionSize', size),
        ('fragmentationSize',      size),
        ('percentIdentityCutoff',  perc_id),
        ('coreGenomeThreshold',    num_strains)
        ('runMode',                'pan'),
        ('blastWordSize',          word),
        ('frameshift',             1),
        ('overwrite',              1)
    )

    with open(os.path.join(work_dir, 'settings.txt'), 'w') as f:
        out = csv.writer(delimiter = '\t')
        for line in settings:
            out.writerow(line)

def run_panseq(work_dir):

    panseq = find_panseq()

    subprocess.call(panseq, os.path.join(work_dir, 'settings.txt'))

def main():

    args = arguments()

    reqs = find_requirements()

    format_settings(args.fasta_dir, args.work_dir, args.fragment_size,
                    args.percent_id, args.word_size, args.cores)

    run_panseq(args.work_dir)

if __name__ == '__main__':
    main()
