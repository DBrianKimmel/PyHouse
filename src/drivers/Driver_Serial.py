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
from src.utils.tools import PrintBytes


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Startup Details
# 4 = Read / write summary
# 5 = Read / write details
# 6 = Details of device on start
# + = NOT USED HERE
g_logger = None


class SerialProtocol(Protocol):

    m_data = None

    def __init__(self, p_data, p_controller_obj):
        self.m_data = p_data
        self.m_controller_obj = p_controller_obj

    def connectionFailed(self):
        print "Driver_Serial.connectionFailed() - ", self

    def connectionMade(self):
        if g_debug >= 2:
            print 'Driver_Serial.connectionMade() - Connected to Serial Device'  # , dir(self), vars(self)

    def dataReceived(self, p_data):
        if g_debug >= 5:
            print "Driver_Serial.dataReceived() - {0:}".format(PrintBytes(p_data))
        self.m_controller_obj.Message += p_data


class SerialAPI(object):
    """Contains all external commands.
    """
    m_bytes = 0
    m_serial = None

    def twisted_open_device(self, p_controller_obj):
        if g_debug >= 3:
            print "Driver_Serial.twisted_open_device() - Name:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port)
            print "   ", vars(p_controller_obj)
        try:
            self.m_serial = SerialPort(SerialProtocol(self, p_controller_obj), p_controller_obj.Port, reactor, baudrate = p_controller_obj.BaudRate)
        except serial.serialutil.SerialException, e:
            l_msg = "Open failed for Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port), e
            g_logger.error(l_msg)
            if g_debug >= 1:
                print l_msg
            return False
        g_logger.info("Opened Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port))
        if g_debug >= 3:
            print 'Driver_Serial.twisted_open_device() - Serial Device opened.'
        return True

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        if g_debug >= 3:
            print "Driver_Serial.close_device() - Name:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port)
        g_logger.info("Close Device {0:}".format(p_controller_obj.Name))
        self.m_serial.close()

    def fetch_read_data(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj
        l_msg = self.m_controller_obj.Message
        if len(l_msg) > 0:
            if g_debug >= 4:
                print "Driver_Serial.fetch_read_data() - {0:} {1:}".format(self.m_bytes, PrintBytes(l_msg))
                g_logger.debug("Fetch Read Data {0:}".format(PrintBytes(l_msg)))
        p_controller_obj.Message = bytearray()
        return l_msg

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        if g_debug >= 4:
            print "Driver_Serial.write_device() {0:}".format(PrintBytes(p_message))
            g_logger.debug("Writing {0:}".format(PrintBytes(p_message)))
        try:
            self.m_serial.writeSomeData(p_message)
        except (AttributeError, TypeError):
            g_logger.warn("Bad serial write - {0:}".format(PrintBytes(p_message)))
            if g_debug >= 1:
                print "Driver_Serial_write_device() ERROR "
        return


class API(SerialAPI):

    def __init__(self):
        """
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.DrvrSerl')
        if g_debug >= 2:
            print "Driver_Serial.API()"
            g_logger.debug("Initializing.")

    def Start(self, p_controller_obj):
        """
        @param p_controller_obj:is the Controller_Data object for a serial device to open.
        """
        if g_debug >= 2:
            print "Driver_Serial.API.Start() - Name:{0:}".format(p_controller_obj.Name)
        self.m_controller_obj = p_controller_obj
        self.twisted_open_device(p_controller_obj)
        g_logger.info("Started.")
        return True

    def Stop(self):
        if g_debug >= 2:
            print "Driver_Serial.API.Stop()"
        self.close_device(self.m_controller_obj)
        g_logger.info("Stopped.")

# ## END DBK
