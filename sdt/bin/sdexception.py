#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdexception.py 3053 2014-03-10 14:07:17Z jripsl $
#  @version        $Rev: 3053 $
#  @lastrevision   $Date: 2014-03-10 15:07:17 +0100 (Mon, 10 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains exception classes.

Note
    This module doesn't use any other (Synchro-Data) module and thus can be used
    everywhere (even in 'sdapp' module) without circular dependency problem.
"""

class SDException(Exception):
    def __init__(self, code=None, msg=None):
        self.code=code
        self.msg=msg
    def __str__(self):
        return "code=%s,message=%s"%(self.code,self.msg)

class NoTransferWaitingException(SDException):
    pass
class FatalException(SDException):
    pass
class RemoteException(SDException):
    pass