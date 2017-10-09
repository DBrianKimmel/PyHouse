"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_PLM -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_PLM.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2017 by D. Brian Kimmel
@note:      Created on Feb 18, 2010
@license:   MIT License
@summary:   This module is for sending commands to and receiving responses from an Insteon Controller.

Create commands and interpret results from any Insteon controller regardless of interface.
This module carries state information about the controller.
This is necessary since the responses may follow a command at any interval.
Responses do not all have to follow the command that caused them.

TODO:
    Work toward getting one instance per controller.
        We may then need to assign lights to a particular controller if there is more than one in a house.
    implement all-links

"""

__updated__ = '2017-04-30'

#  Import system type stuff
try:
    import Queue
except ImportError:
    import queue as Queue

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_decoder, Insteon_utils, Insteon_Link
from Modules.Families.Insteon.Insteon_constants import MESSAGE_TYPES
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Families.Insteon.Insteon_utils import Util
from Modules.Families.family_utils import FamUtil
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.debug_tools import FormatBytes
LOG = Logger.getLogger('PyHouse.Insteon_PLM    ')

#  Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.6  #  this is for fetching data in the rx buffer

#  Modes for setting PLM mode
MODE_DISABLE_DEADMAN = 0x10
MODE_DISABLE_AUTO_LED = 0x20
MODE_MONITOR = 0x40
MODE_DISABLE_AUTO_LINK = 0x80

#  Message flag bits (Page 55 of Developers Manual).
FLAG_BROADCAST_NAK = 0x80
FLAG_ALL_LINK = 0x40
FLAG_ACKNOWLEDGEMENT = 0x20
FLAG_EXTENDED_CMD = 0x10
FLAG_HOPS_LEFT = 0x0C
FLAG_MAX_HOPS = 0x03


class ControllerData(InsteonData):
    """Holds statefull information about a single Insteon controller device.

    There are several different control devices - this is 2412x and 2413x
    where x is 'S' for serial interface and 'U' for a USB interface.

    The USB controller that I have actually uses the Serial protocol so the serial driver
    is used.

    Although there is a manual for Insteon controllers, much of the development was empirically derived.
    For this reason, there is a whole lot of debugging code and output.
    """

    def __init__(self):
        """
        Command 1 and 2 hold the values sent to the device.
        This is so that the return values received later can be correlated to the command we last sent to the device.
        """
        super(ControllerData, self).__init__()
        self._Command1 = None
        self._Command2 = None



class Commands(object):

    @staticmethod
    def _queue_60_command(p_controller_obj):
        """Get IM info (2 bytes).
        See p 273 of developers guide.
        PLM will respond with a 0x60 response.
        """
        LOG.info("Command to get IM info (60)")
        l_command = Insteon_utils.create_command_message('plm_info')
        Insteon_utils.queue_command(p_controller_obj, l_command)

    @staticmethod
    def _queue_62_command(p_controller_obj, p_obj, p_cmd1, p_cmd2):
        """Send Insteon Standard Length Message (8 bytes) (SD command).
        or Extended length (22 Bytes) (ED command)
        See page 230(243) of 2009 developers guide.

        @param p_obj: is the device object.
        @param p_cmd1: is the first command byte
        @param p_cmd2: is the second command byte

        [0] = x02
        [1] = 0x62
        [2-4] = to address
        [5] = Message Flags
        [6] = Command 1
        [7] = Command 2
        (8-21) = Extended data in ED type
        """
        try:
            l_command = Insteon_utils.create_command_message('insteon_send')
            Util.int2message(p_obj.InsteonAddress, l_command, 2)
            l_command[5] = FLAG_MAX_HOPS + FLAG_HOPS_LEFT  #  0x0F
            l_command[6] = p_obj._Command1 = p_cmd1
            l_command[7] = p_obj._Command2 = p_cmd2
            Insteon_utils.queue_command(p_controller_obj, l_command)
            # LOG.info('Send Command: {}'.format((l_command)))
        except Exception as _e_err:
            LOG.error('Error creating command: {}\n{}\n>>{}<<'.format(_e_err, PrettyFormatAny.form(p_obj, 'Device'), FormatBytes(l_command)))

    @staticmethod
    def queue_6B_command(p_controller_obj, p_flags):
        """Set IM configuration flags (3 bytes).
        See page 271  of Insteon Developers Guide.
        """
        LOG.info("Command to set PLM config flag (6B) - to {:#X}".format(p_flags))
        l_command = Insteon_utils.create_command_message('plm_set_config')
        l_command[2] = p_flags
        Insteon_utils.queue_command(p_controller_obj, l_command)

    @staticmethod
    def queue_6C_command(p_controller_obj):
        pass

    @staticmethod
    def queue_6D_command(p_controller_obj):
        pass

    @staticmethod
    def queue_6E_command(p_controller_obj):
        pass

    @staticmethod
    def queue_70_command(p_controller_obj):
        pass

    @staticmethod
    def queue_71_command(p_controller_obj):
        pass

    @staticmethod
    def queue_72_command(p_controller_obj):
        """RF Sleep"""
        pass

    @staticmethod
    def queue_73_command(p_controller_obj):
        """Send request for PLM configuration (2 bytes).
        See page 270 of Insteon Developers Guide.
        """
        LOG.info("Command to get PLM config (73).")
        l_command = Insteon_utils.create_command_message('plm_get_config')
        Insteon_utils.queue_command(p_controller_obj, l_command)



class PlmDriverProtocol(Commands):
    """
    Check the command queue and send the 1st command if available.
    check the plm for received data
    If nothing to send - try again in X seconds.
    if nothing received, try again in Y seconds.
    """

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initializing PLM Device Driver Protocol.")
        p_controller_obj._Queue = Queue.Queue(300)
        self.m_decoder = Insteon_decoder.DecodeResponses(p_pyhouse_obj, p_controller_obj)
        self.dequeue_and_send(p_controller_obj)
        self.receive_loop(p_controller_obj)
        LOG.info("Finished initializing PLM Device Driver Protocol.")

    def driver_loop_stop(self):
        LOG.info('Stopped.')
        pass

    def dequeue_and_send(self, p_controller_obj):
        """Check the sending queue every SEND_TIMEOUT seconds and send if
        anything to send.

        Uses twisted to get a callback when the timer expires.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send, p_controller_obj)
        #  LOG.info('Within send loop.  Size: {}'.format(p_controller_obj._Queue.qsize()))
        try:
            l_command = p_controller_obj._Queue.get(False)
            #  LOG.info('Got command:  {}'.format((l_command)))
        except Queue.Empty:
            return
        if p_controller_obj._DriverAPI != None:
            # LOG.info("Send to PLM:{}, Message:{}".format(p_controller_obj.Name, FormatBytes(l_command)))
            p_controller_obj._Command1 = l_command
            p_controller_obj._DriverAPI.Write(l_command)
        else:
            LOG.error('UhOh - No driver for {}'.format(p_controller_obj.Name))

    def _append_message(self, p_controller_obj):
        """
        Accumulate data received
        """
        l_msg = p_controller_obj._DriverAPI.Read()
        p_controller_obj._Message.extend(l_msg)
        return p_controller_obj._Message  #  For debugging

    def receive_loop(self, p_controller_obj):
        """Check the driver to see if the controller returned any messages.

        Decode message only when we get enough bytes to complete a message.
        Note that there may be more bytes than we need - preserve them.

        TODO: instead of fixed time, callback to here from driver when bytes are rx'ed.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop, p_controller_obj)
        if p_controller_obj._DriverAPI != None:
            self._append_message(p_controller_obj)
            l_cur_len = len(p_controller_obj._Message)
            if l_cur_len < 2:
                return
            #  LOG.info('Receive message is now {}'.format((p_controller_obj._Message)))
            l_response_len = Insteon_utils.get_message_length(p_controller_obj._Message)
            if l_cur_len >= l_response_len:
                self.m_decoder.decode_message(p_controller_obj)
        else:
            LOG.error('Driver missing for {}'.format(p_controller_obj.Name))


class InsteonPlmCommands(object):

    @staticmethod
    def scan_one_light(p_controller_obj, p_obj):
        """Scan a light.  we are looking for DevCat and any other info about the device.

        @param p_obj: is the object for the device that we will query.
        """
        Commands._queue_62_command(p_controller_obj, p_obj, MESSAGE_TYPES['product_data_request'], 0x00)  #  0x03


class InsteonPlmAPI(object):
    """
    """

    def get_aldb_record(self, p_addr):
        pass

    def put_aldb_record(self, p_addr, p_record):
        pass

    def ping_plm(self, p_controller_obj):
        """Send a command to the plm and get its response.
        """
        return Commands._queue_60_command(p_controller_obj)

    def get_link_records(self, p_controller_obj, p_obj):
        return Insteon_Link.InsteonAllLinks().get_all_allinks(p_controller_obj)


class LightHandlerAPI(object):
    """This is the API for light control.
    """

    def start_controller_driver(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        l_msg = "Controller:{}, ".format(p_controller_obj.Name)
        l_msg += "DeviceFamily:{}, ".format(p_controller_obj.DeviceFamily)
        l_msg += "InterfaceType:{}".format(p_controller_obj.InterfaceType)
        LOG.info('Start Controller - {}'.format(l_msg))
        l_driver = FamUtil.get_device_driver_API(p_pyhouse_obj, p_controller_obj)
        p_controller_obj._DriverAPI = l_driver
        l_ret = l_driver.Start(p_pyhouse_obj, p_controller_obj)
        return l_ret

    def stop_controller_driver(self, p_controller_obj):
        if p_controller_obj._DriverAPI != None:
            p_controller_obj._DriverAPI.Stop()

    def set_plm_mode(self, p_controller_obj):
        """Set the PLM to a mode
        """
        LOG.info('Setting mode of Insteon controller {}.'.format(p_controller_obj.Name))
        Commands.queue_6B_command(p_controller_obj, MODE_MONITOR)

    @staticmethod
    def _get_one_device_status(p_controller_obj, p_obj):
        """Get the status of a light.
        We will (apparently) get back a 62-ACK followed by a 50 with the level in the response.
        """
        LOG.info('Request Status from device: {} - {}'.format(p_obj.RoomName, p_obj.Name))
        Commands._queue_62_command(p_controller_obj, p_obj, MESSAGE_TYPES['status_request'], 0)  #  0x19

    @staticmethod
    def _get_one_thermostat_status(p_controller_obj, p_obj):
        """
        Get the status of a thermostat.
        """
        LOG.info('Request Status from thermostat device: {}'.format(p_obj.Name))
        Commands._queue_62_command(p_controller_obj, p_obj, MESSAGE_TYPES['thermostat_status'], 0)  #  0x6A

    @staticmethod
    def _get_engine_version(p_controller_obj, p_obj):
        """ i1 = pre 2007 I think
            i2 = no checksum - new commands
            i2cs = 2012 add checksums + new commands.
        """
        LOG.info('Request Engine version from device: {}'.format(p_obj.Name))
        Commands._queue_62_command(p_controller_obj, p_obj, MESSAGE_TYPES['engine_version'], 0)  #  0x0D

    @staticmethod
    def _get_id_request(p_controller_obj, p_obj):
        """Get the device DevCat
        """
        LOG.info('Request ID(devCat) from device: {}'.format(p_obj.Name))
        Commands._queue_62_command(p_controller_obj, p_obj, MESSAGE_TYPES['id_request'], 0)  #  0x10

    def _get_obj_info(self, p_controller_obj, p_obj):
        self._get_engine_version(p_controller_obj, p_obj)
        self._get_id_request(p_controller_obj, p_obj)
        self._get_one_device_status(p_controller_obj, p_obj)

    def get_all_device_information(self, p_pyhouse_obj, p_controller_obj):
        """Get the status (current level) of all insteon devices.
        """
        LOG.info('Getting information for all Insteon devices.')

        for l_obj in p_pyhouse_obj.House.Lighting.Buttons.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)

        for l_obj in p_pyhouse_obj.House.Lighting.Controllers.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)
                InsteonPlmAPI().get_link_records(p_controller_obj, l_obj)  # Only from controller

        for l_obj in p_pyhouse_obj.House.Lighting.Lights.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)
                # InsteonPlmCommands.scan_one_light(p_controller_obj, l_obj)

        for l_obj in p_pyhouse_obj.House.Hvac.Thermostats.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)

        for l_obj in p_pyhouse_obj.House.Security.GarageDoors.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)

        for l_obj in p_pyhouse_obj.House.Security.MotionSensors.values():
            if l_obj.DeviceFamily == 'Insteon' and l_obj.Active:
                self._get_obj_info(p_controller_obj, l_obj)


class Utility(LightHandlerAPI):
    """
    """

    def start_controller_and_driver(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_pyhouse_obj: is the master obj
        @param p_controller_obj: is the particular controller that we will be starting

        """
        LOG.info('Starting Controller:{}'.format(p_controller_obj.Name))
        l_ret = self.start_controller_driver(p_pyhouse_obj, p_controller_obj)
        if l_ret:
            LOG.info('Controller Driver Start was OK.')
            self.m_protocol = PlmDriverProtocol(p_pyhouse_obj, p_controller_obj)
            self.set_plm_mode(p_controller_obj)
            self.get_all_device_information(p_pyhouse_obj, p_controller_obj)
        else:
            LOG.error('Insteon Controller start failed')
        return l_ret

    def get_plm_info(self, p_pyhouse_obj, p_controller_obj):
        pass

    @staticmethod
    def _format_address(p_addr):
        l_ret = 'Address:({:x}.{:x}.{:x})'.format(p_addr[0], p_addr[1], p_addr[2])
        return l_ret


class API(Utility):

    m_controller_obj = None

    def __init__(self):
        pass

    def _put_controller(self, p_controller_obj):
        """ used in testing to load the controller info to be used in testing.
        """
        self.m_controller_obj = p_controller_obj


    def _get_controller(self):
        """ used in testing to load the controller info to be used in testing.
        """
        return self.m_controller_obj

    def Start(self, p_pyhouse_obj, p_controller_obj):
        """
        Comes from Insteon_device.API.Start()
        Note that not all insteon devices are known when we start.

        @param p_controller_obj: is the controller we are starting
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        l_ret = self.start_controller_and_driver(p_pyhouse_obj, p_controller_obj)
        self.get_plm_info(p_pyhouse_obj, p_controller_obj)
        LOG.info('Started.')
        return l_ret


    def Stop(self, p_controller_obj):
        self.m_protocol.driver_loop_stop()
        self.stop_controller_driver(p_controller_obj)
        LOG.info('Stopped.')


    def ChangeLight(self, p_device_obj, _p_source, p_level, p_rate=0):
        """
        Send a command to change a device (light's level)
        """
        LOG.info("Device Name:{}; to level:{}; at rate:{};".format(p_device_obj.Name, p_level, p_rate))
        if int(p_level) == 0:
            Commands._queue_62_command(self.m_controller_obj, p_device_obj, MESSAGE_TYPES['off'], 0)  #  0x13
        elif int(p_level) == 100:
            Commands._queue_62_command(self.m_controller_obj, p_device_obj, MESSAGE_TYPES['on'], 255)  #  0x11
        else:
            l_level = int(p_level * 255 / 100)
            Commands._queue_62_command(self.m_controller_obj, p_device_obj, MESSAGE_TYPES['on'], l_level)  #  0x11

#  ## END DBK
