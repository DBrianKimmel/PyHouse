"""
@name: PyHouse/Modules/hvac/test/test_thermostat.py

Created on Apr 14, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.utils import xml_tools
from test import xml_data
from Modules.Core.data_objects import PyHouseData

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

# ## END DBK
