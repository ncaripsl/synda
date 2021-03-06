#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module displays files reduced informations.

Note
    This filter is intended to be chained to the file pipeline output.
"""

import sys
import argparse
import json
import humanize
import sdapp
import sdconst
import sdstatutils

def run(files):
    total=sdstatutils.get_total(files)
    statuses=sdstatutils.get_statuses(files)
    print_summary(statuses,total)

    #(projects,models)=get_details(files)
    #print_details(projects,models)

def print_summary(statuses,total,mode='line'):
    if mode=='delimited':
        print "Total size;Pending size;Local size;Total files count;Pending files count;Local files count"
        print "%s;%s;%s;%s;%s;%s"%( humanize.naturalsize(total['all']['size'],gnu=False),
                                    humanize.naturalsize(total['pending']['size'],gnu=False),
                                    humanize.naturalsize(statuses['done']['size'],gnu=False),
                                    humanize.naturalsize(statuses['new']['size'],gnu=False),
                                    total['all']['count'],
                                    total['pending']['count'],
                                    statuses['done']['count'],
                                    statuses['new']['count'])
    elif mode=='line':
        print "Total files count: %s"%total['all']['count']
        #print "Pending files count: %s"%total['pending']['count']
        for s in statuses.keys():
            count=statuses[s]['count']
            if count>0:
                print "%s files count: %s"%(s.title(),count)
        print "Total size: %s"%humanize.naturalsize(total['all']['size'],gnu=False)
        #print "Pending size: %s"%humanize.naturalsize(total['pending']['size'],gnu=False)
        for s in statuses.keys():
            size=statuses[s]['size']
            if size>0:
                print "%s files size: %s"%(s.title(),humanize.naturalsize(size,gnu=False))

def print_details(files):
        print "Details"
        print '======='
        print "Details regarding files with 'new' status"
        print '========================================='
        print 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
