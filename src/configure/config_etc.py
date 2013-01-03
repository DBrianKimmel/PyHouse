'''
 config_etc.py

Created on Jan 2, 2013

@author: briank

Read the /etc/pyhouse.conf file and use the contents to get the fully qualified path
name of the real/runtime XML config file.
'''

import sys


g_debug = 9


class ConfigEtc(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

def find_etc_config_file():
    """Check for /etc/pyhouse.conf existence.
    If not, ABORT and do not become a daemon.

    @return: the filename we found.
    """
    if g_debug > 0:
        print "config_etc.find_etc_config_file()"
    l_file_name = '/etc/pyhouse.conf'
    try:
        l_file = open(l_file_name, mode = 'r')
    except IOError:
        config_abort()
    l_text = l_file.readlines()
    for l_line in l_text:
        if l_line == '':
            continue
        elif l_line[0] == '#':
            continue
        else:
            l_ret = l_line
            return l_ret
    return None

def config_abort():
    print "Could not find or read '/etc/pyhouse.conf'.  Please create it and rerun PyHouse!"
    sys.exit(1)

# ## END
