"""
@name:      PyHouse/Project/src/Modules/Drivers/Serial/serial_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2014
@summary:   Read and write Serial xml

"""

__updated__ = '2019-07-23'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import SerialControllerInformation
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.SerialXml      ')


class SerialInformation():
    """
    """

    def __init__(self):
        self.Type = 'Serial'
        self.Baud = 0
        self.ByteSize = 8
        self.DsrDtr = False
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = 1.0
        self.XonXoff = False


class Config:
    """
    """

    def load_config(self, p_config, p_obj):
        """
        """
        l_obj = p_obj  # SerialInformation()
        l_required = ['Baud']
        for l_key, l_value in p_config.items():
            if l_key == 'BaudRate':
                l_key = 'Baud'
            setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if hasattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Serial Config is missing an entry for "{}"'.format(l_key))
        return l_obj


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_entry):
        l_serial = SerialControllerInformation()
        l_serial.BaudRate = PutGetXML.get_int_from_xml(p_controller_entry, 'BaudRate', 19200)
        l_serial.ByteSize = PutGetXML.get_int_from_xml(p_controller_entry, 'ByteSize', 8)
        l_serial.DsrDtr = PutGetXML.get_bool_from_xml(p_controller_entry, 'DsrDtr', False)
        l_serial.Parity = PutGetXML.get_text_from_xml(p_controller_entry, 'Parity', 'N')
        l_serial.RtsCts = PutGetXML.get_bool_from_xml(p_controller_entry, 'RtsCts', False)
        l_serial.StopBits = PutGetXML.get_float_from_xml(p_controller_entry, 'StopBits', 1.0)
        l_serial.Timeout = PutGetXML.get_float_from_xml(p_controller_entry, 'Timeout', 1.0)
        l_serial.XonXoff = PutGetXML.get_bool_from_xml(p_controller_entry, 'XonXoff', False)
        return l_serial

    @staticmethod
    def write_interface_xml(p_controller_obj):
        l_xml = ET.Element('Serial')
        try:
            PutGetXML.put_int_element(l_xml, 'BaudRate', p_controller_obj.BaudRate)
            PutGetXML.put_int_element(l_xml, 'ByteSize', p_controller_obj.ByteSize)
            PutGetXML.put_bool_element(l_xml, 'DsrDtr', p_controller_obj.DsrDtr)
            PutGetXML.put_text_element(l_xml, 'Parity', p_controller_obj.Parity)
            PutGetXML.put_bool_element(l_xml, 'RtsCts', p_controller_obj.RtsCts)
            PutGetXML.put_float_element(l_xml, 'StopBits', p_controller_obj.StopBits)
            PutGetXML.put_float_element(l_xml, 'Timeout', p_controller_obj.Timeout)
            PutGetXML.put_bool_element(l_xml, 'XonXoff', p_controller_obj.XonXoff)
        except Exception as e_err:
            LOG.error('Error writing XML - {}'.format(e_err))
        return l_xml

# ## END DBK
