"""
@name: PyHouse/src/Modules/hvac/test/test_thermostat.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 14, 2013
@summary: This module is for testing local node data.


"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData
from Modules.utils import xml_tools
from src.test import xml_data, test_mixin

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

# ## END DBK
