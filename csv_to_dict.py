#!/usr/bin/env python

# @Author 
# Chloe-Agathe Azencott
# chloe-agathe.azencott@mines-paristech.fr
# February 2018

import argparse
import cPickle
import csv
import os
import string
import sys

# Hand processed author names: {anauthor:anauthor_split}
hand_processed_authors = {'Yee Whye Teh': ['Yee Whye', 'Teh'],
                          'Christopher De Sa': ['Christopher', 'De Sa'],
                          'Nicolas Le Roux': ['Nicolas', 'Le Roux'],
                          'Mihaela Van der Schaar': [ 'Mihaela', 'Van der Schaar'],
                          'Hiroshi  Mamitsuka': ['Hiroshi', 'Mamitsuka'],
                          'Patrick van der Smagt': ['Patrick', 'van der Smagt'],
                          'Marwa El Halabi': ['Marwa', 'El Halabi'],
                          'Oisin  Mac Aodha': ['Oisin', 'Mac Aodha'],
                          'Young Hun Jung': ['Young Hun', 'Jung'],
                          'M. Pawan Kumar': ['M', 'Pawan Kumar'],
                          'Elad Yom Tov': ['Elad', 'Yom-Tov'],
                          'Scott Cheng-Hsin Yang': ['Scott Cheng-Hsin', 'Yang'],
                          'wai Keen Vong': ['Wai Keen', 'Vong'],
                          'Kelvin Kai Wing Ng': ['Kelvin Kai Wing', 'Ng'],
                          'Ho Chung Leon Law': ['Ho Chung Leon', 'Law'],
                          'Lars Kai Hansen': ['Lars Kai', 'Hansen'],
                          'Brahim Khalil Abid': ['Brahim Khalil', 'Abid'],
                          'Khan Mohammad Al Farabi': ['Khan Mohammad Al', 'Farabi'],
                          'Morteza Noshad Iranzad': ['Morteza', 'Noshad'],
                          'Shiau Hong Lim': ['Shiau Hong', 'Lim'],
                          'Karthik Abinav Sankararaman': ['Karthik Abinav', 'Sankararaman'],
                          'David Alvarez Melis': ['David', 'Alvarez-Melis'],
                          'Sai Praneeth Reddy Karimireddy': ['Sai Praneeth Reddy', 'Karimireddy'],
                          'Ian En-Hsu Yen': ['Ian En-Hsu', 'Yen'],
                          'S. Sathiya Keerthi': ['S. Sathiya', 'Keerthi'],
                          'S. V. N. Vishwanathan': ['S. V. N.', 'Vishwanathan']
                      } 

# Hand processed papers:
hand_processed_papers = {'16': {'paper_name': 'moellenhoff18'},
                         '26': {'paper_name': 'xu18',
                            'authors': 'Xu, Peng and He, Bryan and De Sa, Christopher and Mitliagkas, Ioannis and Re, Chris'},
                         '74': {'paper_name': 'gao18',
                            'authors': 'Gao, Xiand and Li, Xiaobo and Zhang, Shuzhong'},
                         '158': {'paper_name': 'clemencon18',
                             'authors': 'Cl\'emen\,con, Stephan and Portier, Fran\,cois'},
                         '332': {'paper_name': 'fan18',
                             'authors': 'Fan, Jianqing and Gong, Wenyan and Li, Chris Junchi and Sun, Qiang'},
                         '451': {'paper_name': 'lakshminarayanan18',
                             'authors': 'Lakshminarayanan, Chandrashekar and Szepesvari, Csaba'},
                         '459': {'paper_name': 'ma18',
                             'authors': 'Ma, Yuzhe and Nowak, Robert and Rigollet, Philippe and Zhang, Xuezhou and Zhu, Xiaojin'},
                         '474': {'paper_name': 'jaehnichen18'},
                         '510': {'paper_name': 'elhalabi18'},
                         '522': {'paper_name': 'pati18',
                             'authors': 'Pati, Debdeep and Bhattacharya, Anirban and Yang, Yun'},
                         '564': {'paper_name': 'shah18',
                             'authors': 'Shah, Devavrat and Lee, Christina'}
}


def main():
    """ Process the camera-ready description file downloaded from CMT into a dictionary.

    Example:
        $ python process_folders.py CameraReadyPapers.csv crdict.pickle
    """
    parser = argparse.ArgumentParser(description="Process CMT camera-ready data",
                                     add_help=True)
    parser.add_argument("descr_file",
                        help="camera ready papers description file (.csv)")
    parser.add_argument("descr_pickle",
                        help="camera ready papers description dictionary (.pickle)")
    args = parser.parse_args()

    # Check whether pickle file exists
    if os.path.exists(args.descr_pickle):
        sys.stderr.write("ERROR: pickle file %s exists.\n" % args.descr_pickle)
        sys.exit(-1)

    # Parse the CSV file in a dictionary
    papers_dict = {}
    with open(args.descr_file, 'r') as csvfile:
        csvfile.next() # skip line 1
        csvfile.next() # skip line 2
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            #print len(row)
            [paper_id, paper_title, abstract, authors, t, t, t, t, t] = row
            # Process author names
            for i, anauthor in enumerate(authors.split(";")):
                anauthor = anauthor.split('(')[0]
                anauthor = anauthor.rstrip(' ')
                anauthor = anauthor.rstrip("*")

                if hand_processed_authors.has_key(anauthor):
                    anauthor_split = hand_processed_authors[anauthor]
                else:
                    anauthor_split = anauthor.split()
                    if not len(anauthor_split) == 2:
                        print "ERROR on paper %s: author name is %s" % (paper_id, anauthor)
                        print "Please process manually into hand_processed_authors at the top of this script."
                        sys.exit(-1)

                if i == 0:
                    # Paper name = last name of the first author + 18
                    paper_name = "%s18" % anauthor_split[1]
                    # Initialize bibtex author
                    author_names = '%s, %s' % (anauthor_split[1], anauthor_split[0])
                else:
                    author_names += ' and %s, %s' % (anauthor_split[1], anauthor_split[0])
                    
            papers_dict[paper_id] = {'title': paper_title,
                                     'abstract': abstract,
                                     'paper_name': paper_name.lower(),
                                     'authors': author_names}

            # Corrections
            if hand_processed_papers.has_key(paper_id):
                for k, v in hand_processed_papers[paper_id].iteritems():
                    papers_dict[paper_id][k] = v
            
        csvfile.close()

    # Create unique paper names for redundant names
    paper_ids = [int(k) for k in papers_dict.keys()]
    paper_ids.sort()
    paper_ids = ['%d' % k for k in paper_ids]

    paper_names = {} # paper_name:[paper_id]
    for k, v in papers_dict.iteritems():
        pname = v['paper_name']
        if pname not in paper_names.keys():
            paper_names[pname] = [k]
        else:
            paper_names[pname].append(k)

    for pname, paper_id_list in paper_names.iteritems():
        if len(paper_id_list) > 1:
            # need to create unique identifiers lastname18a, lastname18b, etc
            for i, paper_id in enumerate(paper_id_list):
                uniq_paper_name = '%s%s' % (pname, string.ascii_lowercase[i])
                #print uniq_paper_name
                papers_dict[paper_id]['uniq_paper_name'] = uniq_paper_name



    # Save dictionary
    with open(args.descr_pickle, 'w') as f:
        cPickle.dump(papers_dict, f)
        f.close()


if __name__ == "__main__":
    main()
                