#!/usr/bin/env python

# @Author 
# Chloe-Agathe Azencott
# chloe-agathe.azencott@mines-paristech.fr
# February 2018

import argparse
import cPickle
import csv
import os
import shutil
import string
import sys

def main():
    """Process the output of checkAISTATSpaper.py and move papers that are OK to another folder.

    Example:
        $ python process_log_checker.py papers/log_checker papers papers_ok papers_notok crdict.pickle
    """
    parser = argparse.ArgumentParser(description="Process the output ofcheckAISTATSpaper.py ",
                                     add_help=True)
    parser.add_argument("log_file",
                        help="log file of checkAISTATSpaper.py")
    parser.add_argument("papers_dir",
                        help="folder where papers are")
    parser.add_argument("ok_papers_dir",
                        help="folder where to move papers that are OK")
    parser.add_argument("notok_papers_dir",
                        help="folder where to move papers that are not OK")
    parser.add_argument("descr_pickle",
                        help="camera ready papers description dictionary (.pickle)")
    args = parser.parse_args()

    # Create ok_papers_dir, not_ok_papers_dir
    for out_dir in [args.ok_papers_dir, args.notok_papers_dir]:
        if not os.path.isdir(out_dir):
            sys.stdout.write("Creating %s\n" % out_dir)
            try: 
                os.makedirs(out_dir)
            except OSError:
                if not os.path.isdir(out_dir):
                    raise

    # Load dictionary
    with open(args.descr_pickle, 'r') as f:
        papers_dict = cPickle.load(f)
        f.close()

    # Create paper_name to paper_id lookup dictionary
    paper_id_lookup = {}
    for paper_id, paper in papers_dict.iteritems():
        if paper.has_key('uniq_paper_name'):
            paper_name = "%s.pdf" % paper['uniq_paper_name']
        else:
            paper_name = "%s.pdf" % paper['paper_name']
        paper_id_lookup[paper_name] = paper_id

    # Process log file
    counter = 0
    counter_error = 0
    error_ids = []
    with open(args.log_file) as f:
        current_paper = ''
        for line in f:
            ls = line.split()
            if not len(ls):
                continue
            if ls[0] == 'Testing':
                current_paper = line.split()[2]
                counter += 1
                error_msg = ''
            if 'ERROR' in line:
                msg = line.split('>')[2].split('<')[0]
                msg = msg[3:]
                error_msg += '%s\n' % msg
            if ls[0] == 'Done,':
                # print "done"
                if len(error_msg) or int(line.split()[-2]):
                    counter_error += 1
                    pid = paper_id_lookup[current_paper]
                    print "Formatting error in paper %s" % pid
                    error_ids.append(int(pid))
                    # print "File: %s" % current_paper
                    # print error_msg
                    # print "========"
                    shutil.move(('%s/%s' % (args.papers_dir, current_paper)),
                                ('%s/%s' % (args.notok_papers_dir, current_paper)))
                else:
                    shutil.move(('%s/%s' % (args.papers_dir, current_paper)),
                                ('%s/%s' % (args.ok_papers_dir, current_paper)))
        f.close()

    print "%d papers processed" % counter
    print "%d papers had errors" % counter_error

    error_ids.sort()
    print error_ids

if __name__ == "__main__":
    main()