"""
Created on Feb 27, 2014

@author: briank

Controls pandora playback thru pianobar.

"""

# Import system type stuff
import logging
import subprocess


g_debug = 0
g_logger = logging.getLogger('PyHouse.Pandora     ')


class API(object):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, _p_pyhouses_obj):
        subprocess.Popen('/usr/bin/pianobar')
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

    def UpdateXml (self, p_xml):
        pass


# ## END DBK
