#!/usr/bin/python

"""Configure for PyMh module.
This is a Main Module - always present.
"""


# Import system type stuff
from configobj import ConfigObj
import os

# Import PyMh files


Singletons = {}

Configure_Data = {}
CONFIGDIR = './config/'
Sections = {}

def write_module(self, Dict = {}, Section = 'Default'):
    """Write a conf section"""
    #print ' @@ config_mh.write_module - Sections:', Sections
    for l_file, l_list in Sections.iteritems():
        if Section in l_list:
            l_cfg = ConfigObj(CONFIGDIR + l_file)
            l_cfg[Section] = Dict
            l_cfg.write()
            #print " @@ {0:}.write_module - File:{1:}, Section:{2:}".format(__name__, CONFIGDIR + l_file, Section), Dict
            return
    print "***ERROR in supplied config file update", Section, Dict

class ConfigData(object):

    Combined = {}


class ConfigUtility(ConfigData):

    def _read_all_config(self):
        """Read all the files in the config directory.
        keep a list of sections in each file.
        """
        l_files = os.listdir(CONFIGDIR)
        for l_file in l_files:
            if l_file[0] == '.':
                continue
            #print "Loading file", l_file
            Sections[l_file] = []
            cfg = ConfigObj(CONFIGDIR + l_file)
            Configure_Data.update(cfg)
            for l_key in cfg.keys():
                Sections[l_file].append(l_key)


class ConfigureAPI(ConfigUtility):
    """What the world can see.
    """

    def get_cfg_file(self, p_file):
        """Get a ConfigObj that we can write into.
        """
        cfg = ConfigObj(p_file)
        return cfg

class ConfigureMain(ConfigureAPI):

    def __init__(self):
        self._read_all_config()

    def restart(self):
        """Force a reload of all config parameters.
        Invoked from configure if the dict is empty.
        """
        self._read_all_config()

### END
