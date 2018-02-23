#!/usr/bin/env python

# @Author 
# Chloe-Agathe Azencott
# chloe-agathe.azencott@mines-paristech.fr
# February 2018

import argparse
import cPickle
import os
import shutil
import sys

def main():
    """ Process the camera-ready data downloaded from CMT.

    Example:
        $ python process_folders.py crdict.pickle CameraReadyPapers papers suppmat vXpermissions
    """
    parser = argparse.ArgumentParser(description="Process CMT camera-ready data",
                                     add_help=True)
    parser.add_argument("descr_pickle",
                        help="camera ready papers description dictionary (.pickle)")
    parser.add_argument("cmt_dir",
                        help="folder containing the documents dowloaded from CMT")
    parser.add_argument("papers_dir",
                        help="folder where to store the papers")
    parser.add_argument("supp_dir",
                        help="folder where to store the supplementary files")
    parser.add_argument("permissions_dir",
                        help="folder where to store the permissions")
    args = parser.parse_args()

    # Create papers_dir, permissions_dir if they do not exist
    for out_dir in [args.papers_dir, args.supp_dir, args.permissions_dir]:
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

    paper_ids = [int(k) for k in papers_dict.keys()]
    paper_ids.sort()
    paper_ids = ['%d' % k for k in paper_ids]

    # Process papers
    for paper_id in paper_ids:
        paper_dir = '%s/Paper %s' % (args.cmt_dir, paper_id)
        # check repository exists
        if not os.path.isdir(paper_dir):
            # print paper_dir
            print "ERROR: no camera-ready files for paper %s" % paper_id
            continue
        else:
            submitted_files = os.listdir(paper_dir)            
            # start processing paper
            paper_name = papers_dict[paper_id]['paper_name']
            new_paper_name = paper_name
            if papers_dict[paper_id].has_key('uniq_paper_name'):
                new_paper_name = papers_dict[paper_id]['uniq_paper_name']
                
            # check main paper has correct name
            main_paper = '%s.pdf' % paper_name
            if main_paper not in submitted_files:
                print "ERROR: no main paper for paper %s" % paper_id
                print '\t', main_paper
                print '\t', papers_dict[paper_id]['paper_name']
                print '\t', papers_dict[paper_id]['authors']
                continue
            else:
                submitted_files.pop(submitted_files.index(main_paper))
                # copy file to args.papers_dir
                shutil.copy(('%s/%s' % (paper_dir, main_paper)),
                            ('%s/%s.pdf' % (args.papers_dir, new_paper_name)))

            # check permission file has correct name
            possible_permission_files = [('%sSubmission.pdf' % paper_name),
                                         ('%ssubmission.pdf' % paper_name),
                                         ('%sPermission.pdf' % paper_name),
                                         'pmlr-license-agreement.pdf']
            permission_file = ''
            for ppf in possible_permission_files:
                if ppf in submitted_files:
                    permission_file = ppf
                    break
            if not len(permission_file):
                    print "ERROR: no permission file for paper %s" % paper_id
                    continue
            else:
                submitted_files.pop(submitted_files.index(permission_file))
                # copy file to args.permissions_dir
                shutil.copy(('%s/%s' % (paper_dir, permission_file)),
                            ('%s/%sPermission.pdf' % (args.permissions_dir, new_paper_name)))

            # check whether additional file(s)
            if len(submitted_files):
                # check there's only one supplementary file
                if len(submitted_files) > 1:
                    print "ERROR: too many submitted files for paper %s" % paper_id
                    continue
                else:
                    # check file name
                    supp_file = submitted_files[0]
                    if not supp_file.split(".")[0] == '%s-supp' % (paper_name):
                        print "ERROR: supplementary file for paper %s does not have the right name" % paper_id
                    else:
                        # copy file to args.supp_dir
                        supp_ext = supp_file.split(".")[-1]
                        shutil.copy(('%s/%s' % (paper_dir, supp_file)),
                                    ('%s/%s-supp.%s' % (args.supp_dir, new_paper_name, supp_ext)))
                    
if __name__ == "__main__":
    main()
