#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains paths and configuration parameters."""

import os
import argparse
import ConfigParser
import sdtools
from sdexception import SDException
# this module do not import 'sdapp' to prevent circular reference

def get_data_folder():
    if config.has_option('path','data_path'):
        path=config.get('path','data_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    return  "%s/data"%root_folder

def get_db_folder():
    if config.has_option('path','db_path'):
        path=config.get('path','db_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    return  "%s/db"%root_folder

def get_project_default_selection_file(project):
    path="%s/default_%s.txt"%(selection_default_folder,project)
    return path

def find_selection_file(file):
    if os.path.isfile(file):
        return file
    else:
        return "%s/%s"%(selections_folder,file)

def check_path(path):
    if not os.path.exists(path):
        raise SDException("SDATYPES-101","Path not found (%s)"%path)

def print_(name):
    if name is None:
        # print all configuration parameters

        sdtools.print_module_variables(globals())
    else:
        # print given configuration parameter

        if name in globals():
            print globals()[name]

# Init module.

if 'ST_HOME' not in os.environ:
    raise SDException('SDCONFIG-010',"'ST_HOME' is not set")

root_folder=os.environ['ST_HOME']
tmp_folder="%s/tmp"%root_folder
selections_folder="%s/selection"%root_folder
log_folder="%s/log"%root_folder
conf_folder="%s/conf"%root_folder
bin_folder="%s/bin"%root_folder

selection_default_folder="%s/default"%conf_folder

data_download_script_http="%s/sdget.sh"%bin_folder
data_download_script_gridftp="%s/sdgetg.sh"%bin_folder

logon_script="%s/sdlogon.sh"%bin_folder
cleanup_tree_script="%s/sdcleanup_tree.sh"%bin_folder
default_selection_file="%s/default.txt"%selection_default_folder
configuration_file="%s/sdt.conf"%conf_folder
stacktrace_log_file="%s/stacktrace.log"%log_folder

daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder
daemon_start_script="%s/sdstart.sh"%bin_folder
daemon_stop_script="%s/sdstop.sh"%bin_folder


default_options={'max_parallel_download':'8',
                 'post_processing':'0',
                 'unicode_term':'0',
                 'progress':'1',
                 'onemgf':'false',
                 'check_parameter':'1',
                 'verbosity_level':'info',
                 'scheduler_profiling':'0',
                 'lfae_mode':'abort',
                 'indexes':'esgf-node.ipsl.fr,esgf-data.dkrz.de,esgf-index1.ceda.ac.uk',
                 'default_index':'esgf-node.ipsl.fr',
                 'onemgf':'false',
                 'nearest':'false',
                 'nearest_mode':'geolocation',
                 'incorrect_checksum_action':'remove'}

config = ConfigParser.ConfigParser(default_options)
config.read(configuration_file)

data_folder=get_data_folder()
db_folder=get_db_folder()
db_file="%s/sdt.db"%db_folder

check_path(root_folder)
check_path(selections_folder)
check_path(data_folder)

prevent_daemon_and_modification=True # prevent modification while daemon is running
prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses

max_metadata_parallel_download_per_index=3
syndac_history_path=os.path.expanduser("~/.sdhistory")

http_client='wget' # wget | urllib

daemon_command_name='sdtaskscheduler'

# note that variable below only set which low_level mecanism to use to find the nearest (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))
nearest_schedule='post' # pre | post

mono_host_retry=False
proxymt_progress_stat=False
poddlefix=True

twophasesearch=False # Beware before enabling this: must be well tested/reviewed as it seems to currently introduces regression.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None)
    args = parser.parse_args()

    print_(args.name)
