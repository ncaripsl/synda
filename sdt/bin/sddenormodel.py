#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Denormalize model names as search-API don't understand normalized model name."""

import sys
import argparse
import json
import sdapp
import sdparam
import sdprint

def run(facets_groups):
    facets_groups_new=[]

    for facets_group in facets_groups:
        facets_group=denormalize_models(facets_group)
        facets_groups_new.append(facets_group)

    return facets_groups_new

def denormalize_models(facets_group):
    if 'model' in facets_group:
        facets_group['model']=sdparam.denormalize_models_list(facets_group['model'])

    return facets_group

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
