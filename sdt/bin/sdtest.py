#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdtest.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12611 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

from tabulate import tabulate
import argparse
import random
import sdapp
import sdquicksearch
import sdindex
import sdpipeline
import sdparam
import sdsample
from sdtypes import Dataset
from sdprogress import ProgressThread

def test_index_hosts():
    print "ESGF indexes benchmark"
    print "======================"
    print ""

    ProgressThread.start(running_message='Building test query.. ',spinner_type=0,sleep=0.2,end_message=None)

    #parameter=get_test_query()
    parameter=get_random_test_query()

    parameter.append("limit=0")

    test_queries=sdpipeline.build_queries(parameter=parameter,index_host='<index_host>',load_default=False)

    ProgressThread.stop()

    test_query=test_queries[0]
    print "Test query"
    print "----------"
    print "%s"%test_query['url']
    print ""

    ProgressThread.start(running_message='Test running.. ',spinner_type=0,sleep=0.2,end_message=None)

    li=[]
    for index_host in sdindex.index_host_list:
        result=sdquicksearch.run(index_host=index_host,parameter=parameter)
        li.append([index_host,result.num_found,result.call_duration if result.call_duration>=1 else 0.1])

    ProgressThread.stop()
    print "Result"
    print "------"
    li=sorted(li, key=lambda record: record[2])
    print tabulate(li,headers=['Index host','File count','Call duration (seconds)'],tablefmt="plain")

def get_random_test_query():
    datasets=sdsample.get_sample_datasets('CMIP5',1000)
    dataset=random.choice(datasets.files)
    dataset=Dataset(**dataset)

    r=dataset.realm
    t=dataset.time_frequency
    v=random.choice(dataset.variable)

    test_query=["project=CMIP5","variable=%s"%v,"realm=%s"%r,"time_frequency=%s"%t]

    return test_query

def get_test_query():
    test_query=["project=CMIP5","variable=tas","realm=atmos","time_frequency=mon"]
    return test_query

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--benchmark',action='store_true')
    parser.add_argument('-q','--query',action='store_true',help='Print test query')
    args = parser.parse_args()

    if args.benchmark:
        test_index_hosts()
    elif args.query:
        print " ".join(get_random_test_query())