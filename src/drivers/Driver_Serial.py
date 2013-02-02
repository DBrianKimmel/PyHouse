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
import serial
from twisted.internet import reactor
from subprocess import Popen, PIPE
import re

# Import PyMh files
import lighting
from main.tools import PrintBytes

g_debug = 0

g_logger = None
g_message = bytearray()

callLater = reactor.callLater

RECEIVE_TIMEOUT = 1.0  # this is for polling the device for data to be added to the rx buffer

class SerialDeviceData(lighting.lighting.ControllerData):

    SerialPort = {}
    m_serial = None
    m_message = bytearray()

    def __init__(self):
        self.BaudRate = 0
        self.Port = None


class SerialDriverUtility(SerialDeviceData):

    def parse_dmesg(self):
        """If this is a linux box, parse dmesg and try extracting out the connection.
        """
        p1 = Popen(["dmesg"], stdout = PIPE)
        p2 = Popen(["grep", "usb"], stdin = p1.stdout, stdout = PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        # print output
        l_lines = re.split(r'\n+', output)
        # print l_lines
        l_list = [re.search(r'(\[\S+\]\s+usb.*)', l_entry) for l_entry in l_lines]
        # print l_list
        l_usb = []
        for l_ix in l_list:
            if l_ix == None:
                continue
            l_x = l_ix.group()
            l_usb += l_x
            if g_debug > 8:
                print l_x


class SerialAPI(SerialDriverUtility):
    """Contains all external commands.
    """
    m_bytes = 0

    def open_device(self, p_controler_obj):
        """will open and initialize the serial port.
        """
        if g_debug > 0:
            print "Driver_Serial.open_device() - Name:{0:}, Port:{1:}".format(p_controler_obj.Name, p_controler_obj.Port)
        self.m_bytes = 0
        p_controler_obj.BaudRate = 19200
        p_controler_obj.ByteSize = 8
        p_controler_obj.StopBits = 1.0
        p_controler_obj.Parity = serial.PARITY_NONE
        p_controler_obj.Timeout = 1
        try:
            self.m_serial = serial.Serial(p_controler_obj.Port)
            if g_debug > 0:
                print "Driver_Serial opened port 1"
        except serial.SerialException, erm:
            print "Error - Serial port {0:} has an error in opening port {1:}.".format(p_controler_obj.Name, p_controler_obj.Port), erm
            g_logger.warn("Error - Serial port problem opening {0:} - {1:}".format(p_controler_obj.Name, p_controler_obj.Port))
            return None
        self.m_serial.baudrate = p_controler_obj.BaudRate
        self.m_serial.bytesize = int(p_controler_obj.ByteSize)
        if p_controler_obj.Parity == 'None':
            self.m_serial.parity = serial.PARITY_NONE
        if float(p_controler_obj.StopBits) == 1.0:
            self.m_serial.stopbits = serial.STOPBITS_ONE
        self.m_serial.timeout = float(p_controler_obj.Timeout)
        g_logger.info("Initialized serial port {0:} - {1:} @ {2:} Baud".format(p_controler_obj.Name, p_controler_obj.Port, p_controler_obj.BaudRate))
        return self.m_serial

    def close_device(self):
        """Flush all pending output and close the serial port.
        """
        self.m_serial.close()

    def read_device(self):
        """Read the serial device and add to a buffer to be fetched asynchronously.
        """
        callLater(RECEIVE_TIMEOUT, self.read_device)
        l_buffer = bytearray(256)
        try:
            l_bytes = self.m_serial.readinto(l_buffer)
            self.m_bytes += l_bytes
            self.m_message += l_buffer[:l_bytes]
        except (IOError, AttributeError):
            pass
        except:
            pass
        if self.m_bytes > 0:
            pass

    def fetch_read_data(self):
        l_ret = (self.m_bytes, self.m_message)
        if self.m_bytes > 0:
            # self.m_logger.debug("fetch_read_data() - {0:} {1:}".format(self.m_bytes, PrintBytes(self.m_message)))
            if g_debug > 5:
                print "Driver_Serial.fetch_read_data() - {0:} {1:}".format(self.m_bytes, PrintBytes(self.m_message))
        self.m_bytes = 0
        self.m_message = ''
        return (l_ret)

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        if g_debug > 5:
            print "Driver_Serial.write_device() {0:}".format(PrintBytes(p_message))
        try:
            self.m_serial.write(p_message)
        except:
            pass


class API(SerialAPI):

    def __init__(self):
        """
        """
        if g_debug > 0:
            print "Driver_Serial.__init__()"
        global g_logger, g_message
        g_logger = logging.getLogger('PyHouse.SerialDriver')
        g_logger.debug("Initializing.")
        self.parse_dmesg()
        g_message = bytearray()
        g_logger.debug("Initializied.")

    def Start(self, p_controler_obj):
        """
        @param p_controler_obj:is the Controller_Data object for a serial device to open.
        """
        if g_debug > 0:
            print "Driver_Serial.Start() - Name:{0:}".format(p_controler_obj.Name)
        global g_api
        g_logger.debug("Starting.")
        self.open_device(p_controler_obj)
        self.read_device()
        g_logger.debug("Started.")

    def Stop(self):
        if g_debug > 0:
            print "Driver_Serial.Stop()"
        self.close_device()

# ## END
