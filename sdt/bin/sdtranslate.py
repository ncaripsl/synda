#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdtranslate.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains translation routines."""

def translate_name(facets_group,rules):
    facets_group_new={}
    for k,v in facets_group.iteritems():
        new_k=rules[k] if k in rules else k
        facets_group_new[new_k]=v
    return facets_group_new

def translate_value(facets_group,rules):
    keys=facets_group.keys()
    for k in keys:
        d=rules.get(k,{})
        facets_group[k]=translate(facets_group[k],d)

def translate(values,d):
    """Translate values using dictionnary. Values not in dictionnary stay the same."""
    new_values=[]

    for v in values:
        new_v=d[v] if v in d else v
        new_values.append(new_v)

    return new_values