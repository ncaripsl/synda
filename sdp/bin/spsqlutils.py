#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: spsqlutils.py 3049 2014-02-09 15:52:49Z jripsl $
#  @version        $Rev: 3049 $
#  @lastrevision   $Date: 2014-02-09 16:52:49 +0100 (Sun, 09 Feb 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains SQL utils."""

import argparse
import spapp
from spexception import SPException

def get_object_from_resultset(rs,class_):
    kw=resultset_to_dict(rs)
    return class_(**kw)

def get_tablename(o):
    # beware: this method works only if the object name is the same as the table name (case excluded)

    return o.__class__.__name__.lower() # (e.g. File gives "file")

def build_search_placeholder(search_constraints):
    return " AND ".join(["%s=:%s"%(k,k) for k in search_constraints])

def resultset_to_dict(rs):
    kw={}
    for column in rs.keys():
        kw[column]=rs[column]
    return kw

def insert(instance,columns_subset,conn):
    """This func insert data in table using placeholders.

    Note:
        If columns_subset is None, all instance members are inserted.
    """
    def get_dict(instance,keys):
        d={}
        if keys is None:
            d=instance.__dict__
        else:
            for k in keys:
                d[k]=instance.__dict__[k]

        return d

    # create dict containing key/val list to be inserted
    d=get_dict(instance,columns_subset)

    # generate SQL
    tablename=get_tablename(instance)
    columns=', '.join(d.keys())
    placeholders=':'+', :'.join(d.keys())
    query='INSERT INTO %s (%s) VALUES (%s)' % (tablename,columns, placeholders)

    # EXEC
    c = conn.cursor()
    c.execute(query, d) # placeholders resolution take place here
    id_=c.lastrowid
    c.close()

    return id_

def update(instance,columns_subset_without_pk,conn):
    """This func update data in table using placeholders.

    Note:
        - If 'columns_subset_without_pk' is None, all instance members are updated.
    """

    def get_dict(instance,keys,pkname):
        d_without_pk={}

        for k in keys:
            d_without_pk[k]=instance.__dict__[k]

        d_with_pk={pkname:instance.__dict__[pkname]}
        d_with_pk.update(d_without_pk)

        return (d_with_pk,d_without_pk)


    tablename=get_tablename(instance)
    pk=tablename+'_id'

    # create dict containing key/val list to be updated
    (d_with_pk,d_without_pk)=get_dict(instance,columns_subset_without_pk,pk)

    # generate SQL
    pk_placeholders='%s=:%s'%(pk,pk)
    payload_placeholders=', '.join(['%s=:%s'%(k,k) for k in d_without_pk.keys()])
    query='UPDATE %s SET %s WHERE %s' % (tablename, payload_placeholders,pk_placeholders)

    # debug
    #print query
    #print d_with_pk
    #return

    # EXEC
    c = conn.cursor()
    c.execute(query, d_with_pk) # placeholders resolution take place here
    rowcount=c.rowcount
    c.close()

    return rowcount

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()