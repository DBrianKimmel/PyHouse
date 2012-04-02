#!/usr/bin/python

"""Serial Driver module. serial_driver

This module will interface PyMh to a serial device instance.
"""

# Import system type stuff
import logging
import serial
import time
from twisted.internet.task import LoopingCall

# Import PyMh files
import configure_mh
#import insteon_Device
import lighting

g_message = bytearray()


class SerialDriverData(lighting.ControllerData):

    SerialPort = {}
    m_config = None
    m_logger = None
    m_serial = None
    m_message = bytearray()

    def __init__(self, Name):
        #insteon_Device.InsteonControllerData.__init__(self, Name)
        pass


class SerialDriverUtility(SerialDriverData):

    def _print_bytearray(self, p_ba):
        """Print all the bytes of a bytearray as hex bytes.
        """
        l_len = len(p_ba)
        l_message = ''
        if l_len == 0:
            l_message = "<NONE>"
        else:
            for l_x in range(l_len):
                l_message += " {0:#x}".format(p_ba[l_x])
        l_message += " <END>"
        return l_message

    def _serialLoop(self):
        """This is invoked every second.
        It will read and send chars to the serial port.
        It will catch the non-send responses like from a KeyPadLink or Motion Sensor.
        """
        #(la, lb, lc) = self.get_one_message()
        #if la > 0:
        #    print "~~~serial_driver.SerialDriver._serialLoop()"
        self.read_response()

    def get_config(self, p_family, p_key):
        for l_key, l_obj in lighting.Controller_Data.iteritems():
            print " _ serial_driver.get_config ", l_key, l_obj
            if l_key == p_key:
                print " - serial extracting ", p_key
                if l_obj.get_Family == 'Insteon':
                    BaudRate = l_obj.get_BaudRate
                    print " _ serial_driver. ", p_key, p_family, l_key, l_obj
        return l_obj.get_Port(), l_obj.get_BaudRate

        self.m_config = configure_mh.ConfigurePyMh()
        l_dict = self.m_config.get_value('InsteonControllers')
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

    def open_serial(self):
        """will open and initialize the serial port.
        """

    def close_serial(self):
        """Flush all pending output and close the serial port.
        """
        self.m_serial.close()

    def write_command(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
        self.m_serial.write(p_message)
        time.sleep(0.1)

    def read_response(self):
        """Read the serial device.
        Attempt reading till a new read returns nothing.
        Return the bytearray ending with ACK or NAK, hold the rest 
        Returns a a tuple of (int)Bytecount, (bytearray)MessageRead of the size of bytes read.
        Use the read timeout set at init/open time to fetch all the bytes available.
        """
        l_buf = bytearray(256)
        try:
            l_bytes = self.m_serial.readinto(l_buf)
        except:
            l_bytes = 0
        if l_bytes == 0:
            return (0, bytearray())
        self.m_message = l_buf[:l_bytes]
        #self.m_logger.debug("ser_read() - got {0:} bytes ={1:}".format(l_bytes, self._print_bytearray(self.m_message)))
        return (l_bytes, l_buf[:l_bytes])


class SerialDriverMain(SerialDriverAPI):

    def __init__(self, p_family, p_key):
        print "--SerialDriverMain.__init__()", p_family, " ", p_key
        self.m_message = bytearray()
        self.m_logger = logging.getLogger('PyMh.SerialDriver')
        self.m_logger.info(" Initializing serial port")
        Port, BaudRate = self.get_config(p_family, p_key)

        l_ctldat = SerialDriverData(p_key)
        #Port = insteon_Device.InsteonControllerData.get_Port()
        #BaudRate = l_ctldat.get_BaudRate()
        self.m_serial = serial.Serial('/dev/ttyUSB0')
        self.m_serial.baudrate = 19200
        self.m_serial.bytesize = 8
        self.m_serial.parity = serial.PARITY_NONE
        self.m_serial.stopbits = 1
        self.m_serial.timeout = 0.1
        #
        self.m_logger.info("Configure() - serial port {0:} @ {1:}".format(Port, BaudRate))
        self.open_serial()
        LoopingCall(self._serialLoop).start(1)

    def configure(self):
        """Read / reread the config files and set up the SerialPort dict to the given values.
        Set all defaults first tho.
        """
        print "--SerialDriverMain.config()"
        self.m_serial = serial.Serial(self.SerialPort['Port'])
        self.m_serial.baudrate = self.SerialPort['BaudRate']
        self.m_serial.bytesize = self.SerialPort['ByteSize']
        self.m_serial.parity = serial.PARITY_NONE
        self.m_serial.stopbits = 1 # self.SerialPort['StopBits']
        self.m_serial.timeout = self.SerialPort['Timeout']
        self.m_logger.info("Configure() - serial port %s" % (self.SerialPort['Port'],))
        self.open_serial()
        LoopingCall(self._serialLoop).start(1)

### END
