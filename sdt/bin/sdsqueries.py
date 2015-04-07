#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains squeries func.

Notes
    - sdsqueries means 'Synchro-data Serialized queries'.
    - squeries are queries once url is built.
"""
import sdsquery

def print_(squeries):
    for squery in squeries:
        sdsquery.print_(squery)

def get_scalar(squeries,name,default=None,type_=None):
    """This func assume all squery have the same value for this parameter."""
    squery=squeries[0] 
    value=sdsquery.get_scalar(squery,name,default,type_)
    return value
