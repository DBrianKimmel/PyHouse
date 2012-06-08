#!/usr/bin/python

"""Driver_Serial.py - Serial Driver module. 

This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""

# Import system type stuff
import logging
import serial
import time
from twisted.internet.task import LoopingCall

# Import PyMh files
import configure_mh
import lighting
from tools import PrintBytes


Configure_Data = configure_mh.Configure_Data

g_message = bytearray()


class SerialDeviceData(lighting.ControllerData):

    SerialPort = {}
    m_logger = None
    m_serial = None
    m_message = bytearray()

    def __init__(self):
        self.BaudRate = 0
        self.Port = None


class SerialDriverUtility(SerialDeviceData):

    def _serialLoop(self):
        """This is invoked every 1 second.
        """
        self.read_device()

    def get_config(self, p_family, p_key):
        for l_key, l_obj in lighting.Controller_Data.iteritems():
            print " _ Driver_Serial.get_config ", l_key, l_obj
            if l_key == p_key:
                print " - serial extracting ", p_key
                if l_obj.get_Family == 'Insteon':
                    BaudRate = l_obj.get_BaudRate
                    print " _ Driver_Serial. ", p_key, p_family, l_key, l_obj
        return l_obj.get_Port(), l_obj.get_BaudRate

        l_dict = Configure_Data['InsteonControllers']
        self.SerialPort['Port'] = l_dict.get('Port', '/dev/ttyUSB0')
        self.SerialPort['BaudRate'] = l_dict.get('BaudRate', 19200)
        self.SerialPort['ByteSize'] = l_dict.get('ByteSize', 8)
        self.SerialPort['Parity'] = l_dict.get('Parity', 'None')
        self.SerialPort['StopBits'] = l_dict.get('StopBits', 1.0)
        self.SerialPort['Timeout'] = 0.1
        self.SerialPort['WriteTimeout'] = 1
        self.SerialPort['InterCharTimeout'] = 1
        self.SerialPort['XonXoff'] = False
        self.SerialPort['RtsCts'] = False
        self.SerialPort['DsrDtr'] = False


class SerialDriverAPI(SerialDriverUtility):
    """Contains all external commands.
    """

    def open_device(self):
        """will open and initialize the serial port.
        """
        self.m_bytes = 0

    def close_device(self):
        """Flush all pending output and close the serial port.
        """
        self.m_serial.close()

    def read_device(self):
        """Read the serial device and add to a buffer to be fetched asynchronously.
        """
        l_buffer = bytearray(256)
        try:
            l_bytes = self.m_serial.readinto(l_buffer)
            self.m_bytes += l_bytes
            self.m_message += l_buffer[:l_bytes]
        except:
            pass
        if self.m_bytes > 0:
            pass

    def fetch_read_data(self):
        l_ret = (self.m_bytes, self.m_message)
        self.m_bytes = 0
        self.m_message = ''
        return (l_ret)

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        self.m_logger.debug("write_device() - {0:}".format(PrintBytes(p_message)))
        self.m_serial.write(p_message)
        time.sleep(0.1)


class SerialDriverMain(SerialDriverAPI):

    def __init__(self, p_obj):
        """
        @param p_obj:is the Controller_Data object for a serial device to open. 
        """
        self.m_message = bytearray()
        self.m_logger = logging.getLogger('PyHouse.SerialDriver')
        self.m_serial = serial.Serial(p_obj.Port)
        self.m_serial.baudrate = p_obj.BaudRate
        self.m_serial.bytesize = int(p_obj.ByteSize)
        if p_obj.Parity == 'None':
            self.m_serial.parity = serial.PARITY_NONE
        if float(p_obj.StopBits) == 1.0:
            self.m_serial.stopbits = serial.STOPBITS_ONE
        self.m_serial.timeout = float(p_obj.Timeout)
        self.m_logger.info("Initialized serial port {0:} - {1:} @ {2:} Baud".format(p_obj.Name, p_obj.Port, p_obj.BaudRate))
        self.open_device()
        LoopingCall(self._serialLoop).start(1)

### END
