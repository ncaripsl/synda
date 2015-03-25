#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdopenid.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script contains OpenID related functions.

Credit
    https://github.com/stephenpascoe/esgf-pyclient
"""

from xml.etree import ElementTree
import re
import argparse
import sdutils
from sdexception import SDException
import sdnetutils

XRI_NS = 'xri://$xrd*($v*2.0)'
MYPROXY_URN = 'urn:esg:security:myproxy-service'
ESGF_OPENID_REXP = r'https://.*/esgf-idp/openid/(.*)'
MYPROXY_URI_REXP = r'socket://([^:]*):?(\d+)?'

def extract_info_from_openid(openid):
    """Retrieve username,host,port informations from ESGF openID."""

    xrds_buf=sdnetutils.HTTP_GET(openid)
    (hostname,port)=parse_XRDS(xrds_buf)
    username=parse_openid(openid)
    return (hostname,port,username)

def parse_XRDS(XRDS_document):
    xml = ElementTree.fromstring(XRDS_document)

    hostname = None
    port = None
    username = None

    services = xml.findall('.//{%s}Service' % XRI_NS)
    for service in services:
        try:
            service_type = service.find('{%s}Type' % XRI_NS).text
        except AttributeError:
            continue

        # Detect myproxy hostname and port
        if service_type == MYPROXY_URN:
            myproxy_uri = service.find('{%s}URI' % XRI_NS).text
            m = re.match(MYPROXY_URI_REXP, myproxy_uri)
            if m:
                hostname, port = m.groups()

    return hostname, port

def parse_openid(openid):

    # In standard ESGF pattern, openID contains the username
    m = re.match(ESGF_OPENID_REXP, openid)
    if m:
        username = m.group(1)
    else:
        raise SDException('SDOPENID-001','Incorrect format')

    return username

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--openid',default="https://esgf-node.ipsl.fr/esgf-idp/openid/raciazek")
    args = parser.parse_args()

    (hostname,port,username)=extract_info_from_openid(args.openid)

    print "Username: %s"%username
    print "Myproxy hostname: %s"%hostname
    print "Myproxy port: %s"%port