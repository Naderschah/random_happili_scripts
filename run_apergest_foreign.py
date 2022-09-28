#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:51:38 2020

@author: kutkin
"""

import os
import sys
import socket
from apergest.apergest import apergest
from multiprocessing import Pool
import subprocess
import logging
import pandas as pd
from argparse import ArgumentParser

happili = socket.gethostname()
happili = 'happili-04'
home = os.path.expanduser('~')

def setup_logging(verbose=False):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


#%% Apergest

# sync ingest status file:
def sync_ingest_status():
    print('ingest for: ',happili)
    local = '/home/kutkin/apergest/{0}/ingest_done_{1}.txt'.format(happili, happili[-2:])
    moss = '/home/moss/apergest/{0}/ingest_done_{1}.txt'.format(happili, happili[-2:])
    semler = '/home/semler/apergest/{0}/ingest_done_{1}.txt'.format(happili, happili[-2:])
    if happili[-2:] == '01': local = '/home/semler/kutkin_ingest_copy.txt'
    logging.info('Local ingest status file %s', local)
    logging.info('Remote ingest status file %s', moss)
    df1 = pd.read_csv(moss, comment='#')
    df2 = pd.read_csv(local, comment='#')
    df3 = pd.read_csv(semler, comment='#')
    df = pd.concat([df1, df2, df3], ignore_index=True, sort=True).drop_duplicates()
    logging.info('Overwriting ingest status file %s', local)
    df.to_csv(local, index=False)

# # for tid in tids:
def run_apergest(tid, delete=False, force=False, hostname=None):
    logging.info('Ingesing %s', tid)
    apergest_dir = home + "/apergest/{}".format(happili)
    os.chdir(apergest_dir)
    apergest(tid, do_make_jsons=True, do_prepare_ingest=True,dry_run=False,
               do_run_ingest=True, do_delete_data=delete, force=force, hostname=hostname)


def ils(tid):
    beams = ['{:02d}'.format(b) for b in range(40)]
    failed = []
    ingested = []
    for beam in beams:
        try:
            res = subprocess.check_output('ils /altaZone/archive/apertif_main/visibilities_default/{}_AP_B0{}'.format(tid, beam), shell=True)
            ingested.append(beam)
        except:
            failed.append(beam)
            logging.info('No data for beam: {}'.format(beam))
    print('Ingested:', ingested)
    print('Not ingested:', failed)


def parse_args():
    parser = ArgumentParser(description='run apergest')
    parser.add_argument('-i', '--info', help='show which beams were not ingested', action='store_true')
    parser.add_argument('-l', '--local', help='skip synchronizing ingest status files', action='store_true')
    parser.add_argument('-f', '--force', help='force ingest w/out checking the ingest file', action='store_true')
    parser.add_argument('-d', '--delete', help='delete files', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('tid', type=int, nargs='+', help='TaskID(s) to process')
    return parser.parse_args()

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    args = parse_args()
    setup_logging(args.verbose)
    for tid in args.tid:
        if args.info:
            ils(tid)
            continue
            # sys.exit(0)
        if not args.local:
            sync_ingest_status()

        run_apergest(tid, delete=args.delete, force=args.force ,hostname=happili)


# # p = Pool()
# # p.map(fun, tids)

# #%% Apergest

# # # tid = int(sys.argv[1])
# tids = [
#         200928041
#         ]

# for tid in tids:
#     apergest_dir = "/home/kutkin/apergest/{}".format(happili)
#     os.chdir(apergest_dir)

#     apergest(tid, do_make_jsons=True, do_prepare_ingest=True,
#                 do_run_ingest=True, do_delete_data=False)

#     apergest(tid, do_delete_data=True)
    # print(subprocess.check_output('du -sh /data/apertif/{}'.format(tid), shell=True).decode('utf-8'))
