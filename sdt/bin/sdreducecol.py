#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdreducecol.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script remove unused columns."""

import sys
import argparse
import json
import sdapp
from sdtypes import File
import sdlog
import sdprint

def run(files):
    files=remove_unused_fields(files)
    files=remove_facets(files)
    return files 

def remove_unused_fields(files):
    for file in files:
        for k in [ 'index_node'
                  ,'instance_id'
                  ,'cf_standard_name'
                  ,'drs_id'
                  ,'format'
                  ,'metadata_format'
                  ,'variable_long_name'
                  ,'variable_units'
                  ,'forcing'
                  ,'description'
                  ,'master_id'
                  ,'master_gateway']:
            try:
                del file[k]
            except KeyError:
                pass
    return files

def remove_facets(files):
    """
    Note
     'variable', 'project' and 'model' facets are kept.
    """
    for file in files:
        for k in [ 'realm'
                  ,'institute'
                  ,'ensemble'
                  ,'cmor_table'
                  ,'product'
                  ,'experiment'
                  ,'time_frequency']:
            try:
                del file[k]
            except KeyError:
                pass
    return files

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    files=run(files)

    sdprint.print_format(files,args.format,args.print_only_one_item)