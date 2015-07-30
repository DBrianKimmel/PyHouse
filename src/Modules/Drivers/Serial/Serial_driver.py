"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Serial.test.test_Serial_driver -*-

@name:      PyHouse/src/Modules/Drivers/Serial/Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Feb 18, 2010
@license:   MIT License
@summary:   This module is for driving serial devices


This will interface various PyHouse modules to a serial device.

This may be instanced as many times as there are serial devices to control.
Some serial USB Dongles also are controlled by this driver as they emulate a serial port.

"""

# Import system type stuff
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort

# Import PyMh files
from Modules.Utilities.tools import PrintBytes
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.SerialDriver   ')


class SerialProtocol(Protocol):
    """
    A very simple twisted protocol.
    Addumulate the data receivess into a buffer for the controller.
    """

    m_controller_obj = None

    def __init__(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj

    def connectionLost(self, reason):
        LOG.error('Connection lost for controller {} - {}'.format(self.m_controller_obj.Name, reason))

    def connectionMade(self):
        LOG.info('Connection made for controller {}'.format(self.m_controller_obj.Name))

    def dataReceived(self, p_data):
        self.m_controller_obj._Data += p_data


class SerialAPI(object):
    """
    This is a stateful factory for the serial protocol.
    """
    m_serial = None

    def open_serial_driver(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_controller_obj: is the controller information for the serial controller we are opening.
        @return: True if the driver opened OK and is usable
                 False if the driver is not functional for any reason.
        """
        p_controller_obj._Data = ''
        try:
            self.m_serial = SerialPort(SerialProtocol(p_controller_obj), p_controller_obj.Port,
                    p_pyhouse_obj.Twisted.Reactor, baudrate = p_controller_obj.BaudRate)
        except Exception as e_err:
            LOG.error("ERROR Open failed for Device:{}, Port:{} - {}".format(p_controller_obj.Name, p_controller_obj.Port, e_err))
            return False
        LOG.info("Opened Device:{}, Port:{}".format(p_controller_obj.Name, p_controller_obj.Port))
        return True

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        LOG.info("Close Device {}".format(p_controller_obj.Name))
        if self.m_serial != None:  #  not currently open
            self.m_serial.close()
        self.m_serial = None

    def fetch_read_data(self, p_controller_obj):
        l_msg = p_controller_obj._Data
        p_controller_obj._Data = bytearray()
        return l_msg

    def write_device(self, p_message):
        """Send the command to the PLM.
        """
        if self.m_active:
            try:
                self.m_serial.writeSomeData(p_message)
            except (AttributeError, TypeError) as e_err:
                LOG.warning("Bad serial write - {} {}".format(e_err, PrintBytes(p_message)))
        return


class API(SerialAPI):
    """
    This is the standard Device Driver interface.
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_controller_obj: is the Controller_Data object for a serial device to open.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        l_ret = self.open_serial_driver(p_pyhouse_obj, p_controller_obj)
        self.m_active = l_ret
        if l_ret:
            LOG.info("Started Serial controller {}".format(self.m_controller_obj.Name))
        else:
            LOG.error('ERROR - failed to start Serial controller {}'.format(self.m_controller_obj.Name))
        return l_ret

    def Stop(self):
        self.close_device(self.m_controller_obj)
        LOG.info("Stopped controller {}".format(self.m_controller_obj.Name))

    def Read(self):
        """
        Non-Blocking read from the serial port.
        """
        return self.fetch_read_data(self.m_controller_obj)

    def Write(self, p_message):
        """
        Non-Blocking write to the serial port
        """
        # LOG.info('Writing - {}'.format(PrintBytes(p_message)))
        self.write_device(p_message)

# ## END DBK
