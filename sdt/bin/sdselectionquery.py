#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains selection queries."""

import sdapp
from sdexception import SDException

def get_selection_files_list(self,us):
    li=[]
    c = self._conn.cursor()
    c.execute("select t.local_path local_path from selection__transfer ust,transfer t where ust.transfer_id=t.transfer_id and ust.selection_id=?",(us.getselectionid(),))
    rs=c.fetchone()
    while rs!=None:
        li.append(rs["local_path"])
        rs=c.fetchone()
    c.close()

    return li

def get_selection_total_size(us):
    """
    TODO
    for status in sdconst.TRANSFER_STATUSES_ALL:
        (waiting_size,waiting_count)=CDatabaseStats.getselectionstats(us,"waiting")
        (error_size,error_count)=CDatabaseStats.getselectionstats(us,"error")
        (done_size,done_count)=CDatabaseStats.get_selectionstats(us,"done")
        (running_size,running_count)=CDatabaseStats.get_selectionstats(us,"running")
    """
    size=0
    c = sddb.conn.cursor()
    c.execute("select sum(t.size) size from selection__transfer ust,file t where ust.transfer_id=t.transfer_id and ust.selection_id=?",(us.getselectionid(),))
    rs=c.fetchone()
    if rs is not None:
        size=rs[0]
    c.close()

    return size

def get_selections_filescount():
    c = sddb.conn.cursor()

    selections=get_selections_files_count_helper()

    for selection_id in selections.keys():
        c.execute("select filename from selection where selection_id=?",(selection_id,))
        rs=c.fetchone()

        if rs is None:
            raise SDException("SDSTAT-ERR240","Selection not found (%i)"%selection_id)

        filename=rs[0]
        selections[selection_id]['FILENAME']=filename

    c.close()

    return selections

def get_selections_files_count_helper():
    selections={}

    c = sddb.conn.cursor()
    c.execute("select selection_id,count(*) from selection__transfer group by selection_id")

    """
    the query returns something like:

    1|52435
    2|39644
    3|48411
    """

    rs=c.fetchone()
    while rs is not None:
        selection_id=rs[0]
        count=rs[1]

        selections[selection_id]={'COUNT':count}
        rs=c.fetchone()

    c.close()

    return selections
