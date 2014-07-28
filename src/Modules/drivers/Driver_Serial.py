"""
-*- test-case-name: PyHouse.src.Modules.drivers.test.test_Driver_Serial -*-

@name: PyHouse/src/Modules/drivers/Driver_Serial.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Feb 18, 2010
@license: MIT License
@summary: This module is for driving serial devices


This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.
Some serial USB Dongles also are controlled by this driver as they emulate a serial port.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
import serial

# Import PyMh files
from Modules.Core.data_objects import SerialControllerData
from Modules.utils.tools import PrintBytes
from Modules.utils import pyh_log
from Modules.utils import xml_tools

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.DriverSerial')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """


    def _read_serial_interface_xml(self, p_controller_obj, p_controller_entry):
        l_serial = SerialControllerData()
        l_serial.BaudRate = self.get_int_from_xml(p_controller_entry, 'BaudRate', 19200)
        l_serial.ByteSize = self.get_int_from_xml(p_controller_entry, 'ByteSize', 8)
        l_serial.DsrDtr = self.get_bool_from_xml(p_controller_entry, 'DsrDtr', False)
        l_serial.Parity = self.get_text_from_xml(p_controller_entry, 'Parity', 'N')
        l_serial.RtsCts = self.get_bool_from_xml(p_controller_entry, 'RtsCts', False)
        l_serial.StopBits = self.get_float_from_xml(p_controller_entry, 'StopBits', 1.0)
        l_serial.Timeout = self.get_float_from_xml(p_controller_entry, 'Timeout', 1.0)
        l_serial.XonXoff = self.get_bool_from_xml(p_controller_entry, 'XonXoff', False)
        # Put the serial information into the controller object
        xml_tools.stuff_new_attrs(p_controller_obj, l_serial)
        return l_serial

    def _write_serial_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'BaudRate', p_controller_obj.BaudRate)
        self.put_int_element(p_xml, 'ByteSize', p_controller_obj.ByteSize)
        self.put_bool_element(p_xml, 'DsrDtr', p_controller_obj.DsrDtr)
        self.put_text_element(p_xml, 'Parity', p_controller_obj.Parity)
        self.put_bool_element(p_xml, 'RtsCts', p_controller_obj.RtsCts)
        self.put_float_element(p_xml, 'StopBits', p_controller_obj.StopBits)
        self.put_float_element(p_xml, 'Timeout', p_controller_obj.Timeout)
        self.put_bool_element(p_xml, 'XonXoff', p_controller_obj.XonXoff)
        return p_xml


class SerialProtocol(Protocol):

    m_data = None

    def __init__(self, p_data, p_controller_obj):
        self.m_data = p_data
        self.m_controller_obj = p_controller_obj

    def connectionFailed(self):
        pass

    def connectionMade(self):
        pass

    def dataReceived(self, p_data):
        self.m_controller_obj._Message += p_data


class SerialAPI(ReadWriteConfigXml):
    """Contains all external commands.
    """
    m_bytes = 0
    m_serial = None

    def twisted_open_device(self, p_controller_obj):
        """
        @return: True if the driver opened OK and is usable
                 False if the driver is not functional for any reason.
        """
        try:
            self.m_serial = SerialPort(SerialProtocol(self, p_controller_obj), p_controller_obj.Port,
                    reactor, baudrate = p_controller_obj.BaudRate)
        except serial.serialutil.SerialException as e:
            l_msg = "ERROR Open failed for Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port), e
            LOG.error(l_msg)
            return False
        LOG.info("Opened Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port))
        return True

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        LOG.info("Close Device {0:}".format(p_controller_obj.Name))
        self.m_serial.close()

    def fetch_read_data(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj
        l_msg = self.m_controller_obj._Message
        if len(l_msg) > 0:
            if g_debug >= 1:
                LOG.debug("Fetch Read Data {0:}".format(PrintBytes(l_msg)))
        p_controller_obj._Message = bytearray()
        return l_msg

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        if g_debug >= 1:
            LOG.debug("Writing {0:}".format(PrintBytes(p_message)))
        if self.m_active:
            try:
                self.m_serial.writeSomeData(p_message)
            except (AttributeError, TypeError) as e:
                LOG.warning("Bad serial write - {0:} {1:}".format(e, PrintBytes(p_message)))
        return


class API(SerialAPI):

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_controller_obj:is the Controller_Data object for a serial device to open.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        self.m_controller_obj = p_controller_obj
        l_ret = self.twisted_open_device(self.m_controller_obj)
        self.m_active = l_ret
        if l_ret:
            LOG.info("Started controller {0:}".format(self.m_controller_obj.Name))
        return l_ret

    def Stop(self):
        self.close_device(self.m_controller_obj)
        LOG.info("Stopped controller {0:}".format(self.m_controller_obj.Name))

    def Read(self):
        l_ret = self.fetch_read_data()
        return l_ret

    def Write(self, p_message):
        self.write_device(p_message)

# ## END DBK
