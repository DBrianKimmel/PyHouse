#!/usr/bin/python

"""Driver_Serial.py - Serial Driver module.

This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses and using different families.

Since most serial devices are now via USB connections, we can try to use USB and fall back to serial
(/dev/ttyUSBx) when needed.
"""

# Import system type stuff
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
import serial

# Import PyMh files
from src.utils.tools import PrintBytes
from src.utils import pyh_log

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Startup Details
# 4 = Read / write summary
# 5 = Read / write details
# 6 = Details of device on start
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.DriverSerial')


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


class SerialAPI(object):
    """Contains all external commands.
    """
    m_bytes = 0
    m_serial = None

    def twisted_open_device(self, p_controller_obj):
        try:
            self.m_serial = SerialPort(SerialProtocol(self, p_controller_obj), p_controller_obj.Port, reactor, baudrate = p_controller_obj.BaudRate)
        except serial.serialutil.SerialException as e:
            l_msg = "Open failed for Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port), e
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
        try:
            self.m_serial.writeSomeData(p_message)
        except (AttributeError, TypeError) as e:
            LOG.warn("Bad serial write - {0:} {1:}".format(e, PrintBytes(p_message)))
        return


class API(SerialAPI):

    def __init__(self):
        if g_debug >= 1:
            LOG.debug("Initializing.")
        pass

    def Start(self, p_controller_obj):
        """
        @param p_controller_obj:is the Controller_Data object for a serial device to open.
        """
        self.m_controller_obj = p_controller_obj
        self.twisted_open_device(self.m_controller_obj)
        LOG.info("Started controller {0:}".format(self.m_controller_obj.Name))
        return True

    def Stop(self):
        self.close_device(self.m_controller_obj)
        LOG.info("Stopped controller {0:}".format(self.m_controller_obj.Name))

    def Read(self):
        pass

    def Write(self, p_message):
        pass

# ## END DBK
