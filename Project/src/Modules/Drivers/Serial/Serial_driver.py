"""
@name:      Modules/Drivers/Serial/Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Feb 18, 2010
@license:   MIT License
@summary:   This module is for driving serial devices


This will interface various PyHouse Device Family modules to a serial device.

This may be instanced as many times as there are serial devices to control.
Some serial USB Dongles also are controlled by this driver as they emulate a serial port.

The overall logic is that:
    the main lighting, irrigation, hvac, security etc logic needs to change some device so
    it issues control messages.  These messages got to a family dispatcher and from there
    go to a Family_device module (or submodule).  There it gets translated to a controller
    specific emssage(s).  These Messages are then sent to a driver of the kind for that
    physical controller.  This is the driver for a serial controller.  It presents a serial
    interface reguardless of the electrical connection.

"""

__updated__ = '2019-07-24'

#  Import system type stuff
import pyudev
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort

#  Import PyMh files
from Modules.Drivers.interface import DriverStatus
from Modules.Core.Utilities.debug_tools import FormatBytes, PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.SerialDriver   ')


class FindPort():
    """ Check the localhost computer for a port that we will use for the device.
    We will use the information to see ???
    """

    def __init__(self):
        #  l_devices = subprocess.call(['lsusb'])
        #  print l_devices
        l_context = pyudev.Context()
        for l_dev in l_context.list_devices(subsystem='tty'):
            if 'ID_VENDOR' not in l_dev:
                continue
            # print(l_dev.device_node)
            pass


class SerialProtocol(Protocol):
    """
    A very simple protocol.
    Accumulate the data received into a buffer for the controller.
    """

    m_controller_obj = None

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj

    def connectionLost(self, reason):
        """ Override

        When something went wrong and we lost contact with the controller

        We should trigger a restart of the controller connection from here.
        """
        LOG.error('Connection lost for controller {}\n\t{}'.format(self.m_controller_obj.Name, reason))
        SerialAPI().try_restart(self.m_pyhouse_obj, self.m_controller_obj)
        #  self.m_controller_obj._DriverAPI.Stop()
        #  self.m_controller_obj._DriverAPI.Start(self.m_pyhouse_obj, self.m_controller_obj)

    def connectionMade(self):
        """ Override

        Used only to log that we are connected to the controller for this driver.
        """
        LOG.info('Connection made for controller {}'.format(self.m_controller_obj.Name))
        self.m_controller_obj._Data = bytearray()

    def dataReceived(self, p_data):
        """ Override

        The controller got some data, Append it to the bytearray buffer.
        """
        _l_len = len(p_data)
        self.m_controller_obj._Data.extend(p_data)
        # LOG.debug('Rxed {} bytes of data {}'.format(_l_len, FormatBytes(p_data)))


class SerialAPI:
    """
    This is a statefull factory for the serial protocol.
    """
    m_serial = None

    def open_serial_driver(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_controller_obj: is the controller information for the serial controller we are opening.
        @return: True if the driver opened OK and is usable
                 False if the driver is not functional for any reason.
        """
        l_serial = None
        p_controller_obj._Data = bytearray()
        l_baud = p_controller_obj.Interface.Baud
        l_port = '/dev/ttyUSB0'  # p_controller_obj.Port
        LOG.debug('Serial Interface {}'.format(PrettyFormatAny.form(p_controller_obj, 'Controller', 160)))
        try:
            l_serial = SerialPort(
                    SerialProtocol(p_pyhouse_obj, p_controller_obj),  #  Factory
                    l_port,
                    p_pyhouse_obj._Twisted.Reactor,
                    baudrate=l_baud)
            LOG.info("Opened Device:{}, Port:{}".format(p_controller_obj.Name, l_port))
            p_controller_obj.Active = True
            l_topic = 'house/driver/serial/status'
            l_obj = DriverStatus()
            l_obj.Status = 'Open'
            p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, l_obj)
        except Exception as e_err:
            LOG.error("ERROR - Open failed for Device:{}, Port:{}\n\t{}".format(
                        p_controller_obj.Name, p_controller_obj.Interface.Port, e_err))
            p_controller_obj.Active = True
        self.m_serial = l_serial
        return l_serial

    def close_device(self, p_controller_obj):
        """Flush all pending output and close the serial port.
        """
        LOG.info("Close Device {}".format(p_controller_obj.Name))
        if self.m_serial != None:  #  not currently open
            self.m_serial.close()
        self.m_serial = None

    def try_restart(self, p_pyhouse_obj, p_controller_obj):
        """ if the connection is somehow broken, try to get connected again.
        Seems to disconnect on power surges.
        """
        try:
            self.close_device(p_controller_obj)
            self.open_serial_driver(p_pyhouse_obj, p_controller_obj)
        except Exception as e_err:
            LOG.error('ERROR Restart failed - Reason: {}'.format(e_err))

    def fetch_read_data(self, p_controller_obj):
        """ This is called periodically to see if there is any data.
        It should be changed to trigger an event if there is data available.
        """
        # LOG.info('Fetch data {}'.format(FormatBytes(p_controller_obj._Data)))
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
                LOG.warning("Bad serial write - {} {}".format(e_err, FormatBytes(p_message)))
        return


class API(SerialAPI):
    """
    This is the standard Device Driver interface.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialize Serial Driver')

    def Start(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_controller_obj: is the ControllerInformation() object for a serial device to open.
        @return: True if the driver opened OK and is usable
                 False if the driver is not functional for any reason.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        FindPort()
        l_ret = self.open_serial_driver(self.m_pyhouse_obj, p_controller_obj)
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
        LOG.info('Writing - {}'.format(FormatBytes(p_message)))
        self.write_device(p_message)

#  ## END DBK
