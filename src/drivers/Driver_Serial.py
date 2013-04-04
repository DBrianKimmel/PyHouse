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
from twisted.internet.serialport import SerialPort, PARITY_NONE, EIGHTBITS, STOPBITS_ONE

# Import PyMh files
from lights import lighting
from utils.tools import PrintBytes

g_debug = 1
# 0 = off
# 1 = major routine entry
# 2 =
# 3 =

g_logger = None

RECEIVE_TIMEOUT = 1.0  # this is for polling the device for data to be added to the rx buffer

class SerialDeviceData(lighting.ControllerData):

    m_serial = None
    m_message = bytearray()

    def __init__(self):
        self.Port = None
        self.BaudRate = 9600
        self.ByteSize = EIGHTBITS
        self.DsrDtr = False
        self.InterCharTimeout = 0
        self.Parity = PARITY_NONE
        self.RtsCts = False
        self.StopBits = STOPBITS_ONE
        self.Timeout = None
        self.WriteTimeout = None
        self.XonXoff = False


class SerialProtocol(Protocol):

    m_data = None

    def __init__(self, p_data):
        self.m_data = p_data

    def connectionFailed(self):
        print "Driver_Serial.connectionFailed() - ", self

    def connectionMade(self):
        if g_debug >= 3:
            print 'Driver_Serial.connectionMade() - Connected to Serial Device', dir(self), vars(self)

    def dataReceived(self, p_data):
        if g_debug >= 3:
            print "Driver_Serial.dataReceived() - {0:}".format(PrintBytes(p_data))
        self.m_data.m_message += p_data


class SerialAPI(object):
    """Contains all external commands.
    """
    m_bytes = 0
    m_serial = None
    m_message = ''

    def twisted_open_device(self, p_controler_obj):
        if g_debug >= 3:
            print "Driver_Serial.twisted_open_device() - Name:{0:}, Port:{1:}".format(p_controler_obj.Name, p_controler_obj.Port)
        self.m_serial = SerialPort(SerialProtocol(self), p_controler_obj.Port, reactor, baudrate = p_controler_obj.BaudRate)
        if g_debug >= 3:
            print 'Driver_Serial.twisted_open_device() - Serial Device', dir(self.m_serial)

    def close_device(self):
        """Flush all pending output and close the serial port.
        """
        self.m_serial.close()

    def fetch_read_data(self):
        l_ret = self.m_message
        if len(self.m_message) > 0:
            if g_debug > 5:
                print "Driver_Serial.fetch_read_data() - {0:} {1:}".format(self.m_bytes, PrintBytes(self.m_message))
        self.m_message = bytearray()
        return l_ret

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        if g_debug > 5:
            print "Driver_Serial.write_device() {0:}".format(PrintBytes(p_message))
        self.m_serial.writeSomeData(p_message)
        return

        try:
            self.m_serial.write(p_message)
        except:
            print "Driver_Serial_write_device() ERROR "


class API(SerialAPI):

    def __init__(self):
        """
        """
        if g_debug > 0:
            print "Driver_Serial.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.SerialDriver')
        g_logger.debug("Initializied.")

    def Start(self, p_controler_obj):
        """
        @param p_controler_obj:is the Controller_Data object for a serial device to open.
        """
        if g_debug > 0:
            print "Driver_Serial.Start() - Name:{0:}".format(p_controler_obj.Name)
        g_logger.debug("Starting.")
        self.twisted_open_device(p_controler_obj)
        g_logger.debug("Started.")

    def Stop(self):
        if g_debug > 0:
            print "Driver_Serial.Stop()"
        self.close_device()

# ## END
