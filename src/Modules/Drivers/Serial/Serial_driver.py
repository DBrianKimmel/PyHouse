"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Serial.test.test_Serial_driver -*-

@name: PyHouse/src/Modules/Drivers/Serial/Serial_driver.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Feb 18, 2010
@license: MIT License
@summary: This module is for driving serial devices


This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.
Some serial USB Dongles also are controlled by this driver as they emulate a serial port.

"""

# Import system type stuff
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
import serial

# Import PyMh files
from Modules.Utilities.tools import PrintBytes
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.SerialDriver   ')


class SerialProtocol(Protocol):

    m_controller_obj = None

    def __init__(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj

    def connectionLost(self, reason):
        LOG.error('The serial driver connection was lost unexpectedly for controller {} - {}'.format(self.m_controller_obj.Name, reason))

    def connectionMade(self):
        LOG.info('Connection Made to {}'.format(self.m_controller_obj.Name))

    def dataReceived(self, p_data):
        LOG.info('Received {}'.format(PrintBytes(p_data)))
        self.m_controller_obj._Message += p_data


class SerialAPI(object):
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
            self.m_serial = SerialPort(SerialProtocol(p_controller_obj), p_controller_obj.Port,
                    reactor, baudrate = p_controller_obj.BaudRate)
        except serial.serialutil.SerialException as e_err:
            LOG.error("ERROR Open failed for Device:{0:}, Port:{1:} - {2:}".format(p_controller_obj.Name, p_controller_obj.Port, e_err))
            return False
        LOG.info("Opened Device:{0:}, Port:{1:}".format(p_controller_obj.Name, p_controller_obj.Port))
        return True

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        LOG.info("Close Device {0:}".format(p_controller_obj.Name))
        if self.m_serial == None:  #  not currently open
            return
        self.m_serial.close()

    def fetch_read_data(self, p_controller_obj):
        l_msg = p_controller_obj._Message
        if len(l_msg) > 0:
            LOG.debug("Fetch Read Data {0:}".format(PrintBytes(l_msg)))
        p_controller_obj._Message = bytearray()
        return l_msg

    def write_device(self, p_message):
        """Send the command to the PLM and wait a very short time to be sure we sent it.
        """
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
            LOG.info("Started Serial controller {0:}".format(self.m_controller_obj.Name))
        else:
            LOG.error('ERROR - failed to start Serial controller {0:}'.format(self.m_controller_obj.Name))
        return l_ret

    def Stop(self):
        self.close_device(self.m_controller_obj)
        LOG.info("Stopped controller {0:}".format(self.m_controller_obj.Name))

    def Read(self):
        """
        Non-Blocking read from the serial port.
        """
        l_ret = self.fetch_read_data(self.m_controller_obj)
        return l_ret

    def Write(self, p_message):
        """
        Non-Blocking write to the serial port
        """
        self.write_device(p_message)

# ## END DBK
