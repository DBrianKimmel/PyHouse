"""
@name: PyHouse/src/hvac/test/test_thermostat.py

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
from src.utils import xml_tools
from src.test import xml_data
from src.core.data_objects import PyHouseData, CoreData

XML = xml_data.XML


class Test_02_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'src.text.xml_data' file is correct and what the node_local module can read/write.
    """

# ## END DBK
