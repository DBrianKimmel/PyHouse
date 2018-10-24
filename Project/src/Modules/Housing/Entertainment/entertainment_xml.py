"""
-*- test-case-name: PyHouse/Project/src/Modules/Housing/Entertainment/entertainment_xml.py -*-

@name:      PyHouse/Project/src/Modules/Housing/Entertainment/entertainment_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Oct 17, 2018
@license:   MIT License
@summary:   Load / Save all the entertainment XML

"""

__updated__ = '2018-10-17'
__version_info__ = (18, 10, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData, \
        EntertainmentDeviceControl
from Modules.Core.Utilities.xml_tools import XmlConfigTools  # , PutGetXML
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.EntertainXML   ')


class XML:
    """
    """

    def LoadXml(self, p_pyhouse_obj):
        """ Read the entertainment section.
        Everything present in the XML must be read into the pyhouse_obj structure.

        SubSections not active will not be loaded or instantiated.

        If a subsection is available, load its module and let it read the xml for itself.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("XML Loading - Version:{}".format(__version__))
        l_entertain = p_pyhouse_obj.House.Entertainment
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        if l_xml == None:
            l_entertain.Active = False
            return l_entertain
        l_count = 0
        for l_section_element in l_xml:
            self._module_load_loop(p_pyhouse_obj, l_section_element)
            l_count += 1
        l_entertain.Active = True
        l_entertain.Count = l_count
        LOG.info('XML Loaded {} Entertainment Sections'.format(l_count))
        return l_entertain

# ## END DBK
