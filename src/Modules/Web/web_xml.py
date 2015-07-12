"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_xml -*-

@name:      PyHouse/src/Modules/Web/web_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import WebData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML

LOG = Logger.getLogger('PyHouse.WebXml         ')


class WebXmlAPI(object):
    """
    """

    def read_web_xml(self, p_pyhouse_obj):
        l_obj = WebData()
        try:
            l_xml = p_pyhouse_obj.XmlRoot.find('WebSection')
            l_obj.WebPort = PutGetXML.get_int_from_xml(l_xml, 'WebPort', 8580)
        except AttributeError:
            l_obj.WebPort = 8580
        return l_obj

    def write_web_xml(self, p_web_obj):
        l_web_xml = ET.Element("WebSection")
        try:
            PutGetXML.put_int_element(l_web_xml, 'WebPort', p_web_obj.WebPort)
        except AttributeError:
            PutGetXML.put_int_element(l_web_xml, 'WebPort', 8580)
        return l_web_xml

# ## END DBK