#!/usr/bin/python

"""Driver_Serial.py - Serial Driver module.

This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses and using different families.

Since most serial devices are now via USB connections, we can try to use USB and fall back to serial
(/dev/ttyUSBx) when needed.
"""

# Import system type stuff
import logging
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
import serial

# Import PyMh files
from utils.tools import PrintBytes
from utils import xml_tools


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Startup Details
# 3 = Read / write summary
# 4 = Read / write details
# 5 = Details of device on start

g_logger = None

RECEIVE_TIMEOUT = 1.0  # this is for polling the device for data to be added to the rx buffer

class ReadWriteConfig(xml_tools.ConfigTools):

    def extract_serial_xml(self, p_controller_obj, p_controller_xml):
        pass

class SerialProtocol(Protocol):

    m_data = None

    def __init__(self, p_data):
        self.m_data = p_data

    def connectionFailed(self):
        print "Driver_Serial.connectionFailed() - ", self

    def connectionMade(self):
        if g_debug >= 2:
            print 'Driver_Serial.connectionMade() - Connected to Serial Device'  # , dir(self), vars(self)

    def dataReceived(self, p_data):
        if g_debug >= 4:
            print "Driver_Serial.dataReceived() - {0:}".format(PrintBytes(p_data))
        self.m_data.m_message += p_data


class SerialAPI(object):
    """Contains all external commands.
    """
    m_bytes = 0
    m_serial = None
    m_message = ''

    def twisted_open_device(self, p_controller_obj):
        if g_debug >= 2:
            print "Driver_Serial.twisted_open_device() - Name:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port)
            print "   ", vars(p_controller_obj)
        try:
            self.m_serial = SerialPort(SerialProtocol(self), p_controller_obj.Port, reactor, baudrate = p_controller_obj.BaudRate)
        except serial.serialutil.SerialException:
            g_logger.error("Open failed for Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port))
            return
        g_logger.info("Opened Device:{0:}, Port:{1:}".format(p_controller_obj.Name))
        if g_debug >= 2:
            print 'Driver_Serial.twisted_open_device() - Serial Device opened.'

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        if g_debug >= 2:
            print "Driver_Serial.close_device() - Name:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port)
        g_logger.info("Close Device {0:}".format(p_controller_obj.Name))
        self.m_serial.close()

    def fetch_read_data(self, p_controller_obj):
        l_ret = self.m_message
        if len(self.m_message) > 0:
            if g_debug >= 3:
                print "Driver_Serial.fetch_read_data() - {0:} {1:}".format(self.m_bytes, PrintBytes(self.m_message))
                g_logger.debug("Fetch Read Data {0:}".format(PrintBytes(self.m_message)))
        self.m_message = bytearray()
        return l_ret

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        if g_debug >= 3:
            print "Driver_Serial.write_device() {0:}".format(PrintBytes(p_message))
            g_logger.debug("Writing {0:}".format(PrintBytes(p_message)))
        self.m_serial.writeSomeData(p_message)
        return

        try:
            self.m_serial.write(p_message)
        except AttributeError:
            print "Driver_Serial_write_device() ERROR "


class API(SerialAPI):

    def __init__(self):
        """
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.DrvrSerl')
        if g_debug >= 1:
            print "Driver_Serial.__init__()"
            g_logger.debug("Initializing.")

    def Start(self, p_controller_obj):
        """
        @param p_controller_obj:is the Controller_Data object for a serial device to open.
        """
        self.m_controller_obj = p_controller_obj
        if g_debug >= 1:
            print "Driver_Serial.Start() - Name:{0:}".format(p_controller_obj.Name)
        self.twisted_open_device(p_controller_obj)
        g_logger.info("Started.")

    def Stop(self):
        if g_debug >= 1:
            print "Driver_Serial.Stop()"
        self.close_device(self.m_controller_obj)
        g_logger.info("Stopped.")

# ## END
