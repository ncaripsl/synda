#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdstatusfilter.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script keeps files with the given status.

Note
    This module is intended to be use in post-call pipeline based on end-user
    choice (to remove status in other places (e.g. to enforce that some status
    are removed no matter what the end-user choice is), use sdsimplefilter
    module).
"""

import sys
import argparse
import json
import sdapp
import sdpostpipelineutils
import sdprint

def run(files):
    new_files=[]

    for f in files:

        # retrieve status attributes
        status=f['status']                                                   # scalar
        status_filter=sdpostpipelineutils.get_attached_parameter(f,'status') # list

        if status_filter is None:
            new_files.append(f)
        else:
            assert isinstance(status_filter,list)
            if status in status_filter:
                new_files.append(f)
            else:
                pass

    return new_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)