#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import time
import argparse
import sdapp
from sdtypes import Request,Response,File
from sdexception import SDException
from sdtime import SDTimer
import sdnetutils
import sdconst
import sdlog
import sdtools
import sdconfig

# not a singleton
class SearchAPIProxy():
    def __init__(self,**kw):
        pass

    def run(self,url=None,attached_parameters={}):
        """Execute one search query (as pagination is used, it can result in many HTTP queries)

        Returns:
            Response object
        """
        request=Request(url=url,pagination=True)
        final_url=request.get_url()

        sdlog.info("SYDPROXY-490","paginated call started (url=%s)"%final_url)

        try:
            result=self.call_web_service__PAGINATION(request) # return Response object
        except Exception,e:
            sdlog.error("SYDPROXY-400","Error occurs during search-API paginated call (url=%s)"%(final_url,))
            sdlog.error("SYDPROXY-410","%s"%(str(e),))
            raise

        sdlog.info("SYDPROXY-001","paginated call completed (call-duration=%i, files-count=%i, url=%s)"%(result.call_duration, len(result.files), final_url))

        if attached_parameters.get('verbose',False) == True:
            sdtools.print_stderr("Url: %s"%final_url)
            sdtools.print_stderr("Duration: %s"%result.call_duration)
            sdtools.print_stderr("")

        result.add_attached_parameters(attached_parameters)
        return result

    def call_web_service(self,request):

        sdlog.debug("SYDPROXY-100","Search-API call started (%s)."%request.get_url())

        try:
            result=sdnetutils.call_web_service(request,sdconst.SEARCH_API_HTTP_TIMEOUT) # returns Response object
        except:

            # if exception occurs in sdnetutils.call_web_service() method, all
            # previous calls to this method inside this paginated call are also
            # cancelled

            # we reset the offset so the paginated call can be restarted from the begining the next time
            # (maybe overkill as offset is reinitialized when entering 'call_web_service__PAGINATION()' func)
            request.offset=0

            raise

        assert result.num_result==len(result.files) # should always be the same

        sdlog.debug("SYDPROXY-100","Search-API call completed (returned-files-count=%i,match-count=%i,url=%s)."%(len(result.files),result.num_found,request.get_url()))

        return result

    def call_web_service__RETRY(self,request):
        """Add mono-host retry to call_web_service() method.

        Notes
            - multi-host retry is available via sdproxy_mt module.
            - when using sdproxy_mt module, this retry is normally not necessary,
              except for one case: it's when one wants to dump huge amount of data from ESGF
              (i.e. not 10 000, but something more like 1 000 000). In this case,
              probability for a failure inside one pagination call is big (because one
              pagination call is composed of many sub calls (i.e. not just 2 or 3)).
        """
        max_retry=3

        i=0
        while True:
            if i>0:
                sdlog.info("SYDPROXY-088","Retry search-API call (%s)."%request.get_url())

            try:
                result=self.call_web_service(request)
                break
            except:
                sdlog.info("SYDPROXY-090","Search-API call failed (%s)."%request.get_url())

                if i>=max_retry:
                    sdlog.info("SYDPROXY-092","Maximum number of retry attempts reached: cancel pagination call (%s)."%request.get_url())
                    raise
                else:
                    i+=1

        return result

    def call_web_service__PAGINATION(self,request):
        """
        Notes
            This function contain paging management (i.e. make web service calls until all results are returned)
        """

        # init
        request.limit=sdconst.CHUNKSIZE
        request.offset=0
        offset = 0
        chunks = []        # list of chunks (every web service call generate one chunk (which is a Response object))
        nread = 0          # how many already read
        moredata = True

        while moredata: # paging loop

            # paging (pre-processing)
            request.offset=offset

            # call
            if sdconfig.mono_host_retry:
                result=self.call_web_service__RETRY(request)
            else:
                result=self.call_web_service(request)

            # retrieve output
            chunks.append(result) # Response object

            # paging (post-processing)
            offset += sdconst.CHUNKSIZE
            nread += result.num_result
            nleft = result.num_found - nread

            moredata = (nleft>0) and (result.num_result>0) # the second member is for the case when "num_found > 0" but nothing is returned

        # merge all chunks
        files=[]
        elapsed_time=0
        for chunk in chunks:
            files.extend(chunk.files)
            elapsed_time+=chunk.call_duration # merge elapsed time


        return Response(files=files,call_duration=elapsed_time) # call_duration here means multi-call duration (i.e. because of pagination)

if __name__ == '__main__':
    search=SearchAPIProxy()
    url="http://esgf-data.dkrz.de/esg-search/search?fields=*&realm=atmos&project=CMIP5&time_frequency=mon&experiment=rcp26&variable=tasmin&model=CNRM-CM5&model=CSIRO-Mk3-6-0&model=BCC-CSM1-1-m&ensemble=r1i1p1&type=File"
    result=search.run(url=url)

    # dict to "File" operation
    file_list=[]
    for file in result.files:
        file_list.append(File(**file))

    for f in file_list:
        print "%s %s"%(f.timestamp,f.id)
