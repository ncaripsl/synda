#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sddb.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12611 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script contains database I/O routines."""

import sqlite3
import atexit
import sdapp
from sdexception import SDException
import sdconfig
import sddbobj

def check_version():
    # this method must stay in this module to prevent any DB I/O if database version does not match binary version

    c = conn.cursor()
    c.execute("select version from version")
    rs=c.fetchone()
    version=rs[0] if rs!=None else None
    c.close()

    if version==None:
        # this case is for when starting from scratch (e.g. when db file as been removed)

        c = conn.cursor()
        c.execute("insert into version (version) values (?)",(sdapp.version,))
        conn.commit()
        c.close()
    else:
        if sdapp.version!=version:
            raise SDException("SYNCDDAO-317","Database must be upgraded: run 'sdupgrade' command")

def connect():
    global conn

    # When a database is accessed by multiple connections, and one of the processes
    # modifies the database, the SQLite database is locked until that transaction is
    # committed. The timeout parameter specifies how long the connection should wait
    # for the lock to go away until raising an exception. The default for the timeout
    # parameter is 5.0 (five seconds).
    #
    # more info here => http://www.sqlite.org/faq.html#q5
    #
    # we increase the timeout so we are able to use sqlite3 to run manual
    # query without stopping the daemon
    #
    l__timeout=120 # 2 mn

    # Note
    #  by default, sqlite is in autocommit mode,
    #  but the sqlite3 python module is *not* in autocommit mode by default
    #  we don't want autocommit mode, so we leave it at its default, which will result in a plain "BEGIN" statement
    #  (If you want autocommit mode, then set isolation_level to None)

    # open connection
    conn=sqlite3.connect(sdconfig.db_file,l__timeout)
    conn.row_factory=sqlite3.Row # this is for "by name" colums indexing

    # create DB object
    sddbobj.create_tables(conn)
    sddbobj.create_indexes(conn)

def disconnect():
    global conn

    if is_connected():
        conn.close()

    conn=None

def is_connected():
    if (conn==None):
        return False
    else:
        return True

def unloadTableFromMemory(tablename):
    _in_memory_conn.execute("drop table if exists main.'%s'"%tablename)

def closeInMemoryDatabase():
    global _in_memory_conn

    _in_memory_conn.close()
    _in_memory_conn=None

def loadTableInMemory(tablename,indexname):
    global _in_memory_conn

    sdlog.log("SDDATABA-INF001","loading '%s' table"%tablename)

    # create a database in memory
    if _in_memory_conn is None:
        _in_memory_conn = sqlite3.connect(":memory:")

    # attach persistent DB
    _in_memory_conn.execute("ATTACH '%s' AS persistentdb"%get_db_name())

    # drop table if already exists in memory
    _in_memory_conn.execute("drop table if exists main.'%s'"%tablename)
    # copy table from persistent DB to memory
    _in_memory_conn.execute("create table main.'%s' as select * from persistentdb.[%s]"%(tablename,tablename))
    # create index
    _in_memory_conn.execute("create index if not exists main.'%s' on '%s' (file)"%(indexname,tablename))

    # commit
    _in_memory_conn.commit()

    # detach persistent DB
    _in_memory_conn.execute("detach persistentdb")  

    _in_memory_conn.row_factory = sqlite3.Row

    #sdlog.log("SDDATABA-INF002","table loaded")

# module init

conn=None
_in_memory_conn=None

connect()
check_version()
atexit.register(disconnect)