"""
Modules/families/UPB/UPB_Pim.py

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright (c) 2010-2014 by D. Brian Kimmel

@license: MIT License

@summary: Handle the controller component of the lighting system.


/srv/backup/home/briank/svn/smarthouse/trunk/Modules/parts/upb/usbhidserial.cpp

Sent to PIM <17>70 03 8D <0D> <2005-09-24 20:58:55 75535.86>
PA <20:58:55 75535.94>

Sent to PIM <14>07 10 01 03 FF 30 B6 <0D> <2005-09-24 20:58:55 75535.94>
PA <20:58:56 75536.03>
PK <20:58:56 75536.24>
PU080001FF03864629 <20:58:56 75536.47>

Sent to PIM <14>07 10 01 02 FF 30 B7 <0D> <2005-09-24 20:58:57 75537.47>
PA <20:58:57 75537.51>
PK <20:58:57 75537.66>
PU080001FF02860070 <20:58:57 75537.86>

Sent to PIM <14>07 10 01 01 FF 30 B8 <0D> <2005-09-24 20:58:58 75538.86>
PA <20:58:58 75538.9>
PK <20:58:59 75539.05>
PU8904010001860600E5 <20:58:59 75539.29>
PU8905010001860600E4 <20:58:59 75539.45>

Sent to PIM <14>07 10 01 00 FF 30 B9 <0D> <2005-09-24 20:59:00 75540.45>
PA <20:59:00 75540.58>
PK <20:59:00 75540.63>
PU8905010001860600E4 <20:59:01 75541.04>
PU080001FF03864629 <20:59:01 75541.26>

Sent to PIM <14>87 10 01 82 FF 20 C7 <0D> <2005-09-24 20:59:21 75561.36>
PA <20:59:21 75561.48>
PK <20:59:21 75561.77>

Sent to PIM <14>07 10 01 03 FF 30 B6 <0D> <2005-09-24 20:59:31 75571.77>
PA <20:59:31 75571.83>
PK <20:59:32 75572.13>
PU080001FF0386006F <20:59:32 75572.58>

Sent to PIM <14>87 10 01 81 FF 20 C8 <0D> <2005-09-24 21:00:33 75633.89>
PA <21:00:33 75633.97>
PK <21:00:34 75634.27>

Sent to PIM <14>07 10 01 03 FF 30 B6 <0D> <2005-09-24 21:00:44 75644.27>
PA <21:00:44 75644.36>
PK <21:00:44 75644.64>
PU080001FF03864629 <21:00:45 75645>

Sent to PIM <14>87 10 01 83 FF 20 C6 <0D> <2005-09-24 21:00:53 75653.08>
PA <21:00:53 75653.16>
PK <21:00:53 75653.47>

Sent to PIM <14>87 10 01 82 FF 20 C7 <0D> <2005-09-24 21:00:53 75653.47>
PA <21:00:53 75653.58>
PK <21:00:53 75653.91>

Sent to PIM <14>07 10 01 02 FF 30 B7 <0D> <2005-09-24 21:01:03 75663.47>
PA <21:01:03 75663.56>
PK <21:01:03 75663.84>
PU080001FF02864B25 <21:01:04 75664.25>



"""

# Import system type stuff
import Queue

# Import PyMh files
from Modules.Core.data_objects import UPBData
from Modules.utils.tools import PrintBytes, PrettyPrintAny
from Modules.utils import pyh_log

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.UPB_PIM     ')


# UPB Control Word
# Page 15
LINK_PKT = 0x80
LOW_REQ = 0x02

ACK_REQ = 0x10
ACK_ID = 0x20
ACK_MSG = 0x40

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for fetching data in the RX buffer


# Command types
CTL_T = 0x14  # transmit a UPB Message
CTL_R = 0x12  # Read PIM Registers
CTL_W = 0x17  # Write PIM Registers


pim_commands = {
# Core commands
'null'                      : 0X00,
'write_enable'              : 0x01,
'write_protect'             : 0x02,
'start_setup_mode'          : 0x03,
'stop_setup_mode'           : 0x04,
'get_setup_time'            : 0x05,
'auto_address'              : 0x06,
'get_device_status'         : 0x07,
'set_device_status'         : 0x08,
'add_link'                  : 0x0B,
'delete_link'               : 0x0C,
'transmit_message'          : 0x0D,
'device_reset'              : 0x0E,
'get_device_signature'      : 0x0F,
'get_register_value'        : 0x10,
'set_register_value'        : 0x11,
# Device Control commands
'activate_link'             : 0x20,
'deactivate_link'           : 0x21,
'goto'                      : 0x22,
'fade_start'                : 0x23,
'fade_stop'                 : 0x24,
'blink'                     : 0x25,
'indicate'                  : 0x26,
'toggle'                    : 0x27,
'report_state'              : 0x30,
'store_state'               : 0x31
}


class BuildCommand(object):
    """
    This class will take a command bytearray and convert it ot a bytearray for sending.

    Write register commands:
    The command for changing register 70's value to 03 is  ==> 70 03.
    First we add a checksum (8D in this case) to the bytearray ==> 70 03 8D.
    next 70 03 8D is converted to 37 30 30 33 38 44 by converting each nibble to an ascii hex value.
    Finally the command becomes 14 37 30 30 33 38 44 0D and is queued for sending
    """

    def _nibble_to_hex(self, p_nibble):
        """Take the low order nibble and convert it to a single byte that is the ascii code for the nibble.

        0x01 ==> 0x31 ('1')
        0x0A ==> 0x41 ('A')
        0x0F ==> 0x46 ('F')
        """
        l_ret = 0x30 + p_nibble
        if l_ret > 0x39:
            l_ret += 0x07
        l_ret = chr(l_ret)
        return ord(l_ret)

    def _byte_to_2chars(self, p_byte):
        """Take a single byte and return 2 bytes that are the ascii hex equivalent.

        0x12 ==> 0x3132 ('12')
        """
        l_ret = bytearray(2)
        l_ret[0] = self._nibble_to_hex(p_byte / 16)
        l_ret [1] = self._nibble_to_hex(p_byte % 16)
        return l_ret

    def _calculate_checksum(self, p_msg):
        """Take a byte array of arbitrary length and return a byte array with the checksum appended to the original.

        b'\x70\x03' ==> b'\x70\x03\x8D'
        """
        l_out = bytearray(0)
        l_cs = 0
        for l_ix in range(len(p_msg)):
            l_byte = ord(p_msg[l_ix])
            l_cs = (l_cs + l_byte) % 256
            l_out.append(l_byte)
        l_out.append(int(256 - l_cs))
        return l_out

    def _convert_pim(self, p_array):
        l_string = chr(CTL_T)  # Transmit a UPB message
        for l_byte in p_array:
            l_char = "{0:02X}".format(l_byte)
            # l_char = chr(l_byte)
            l_string += l_char
        l_string += chr(0x0D)
        if g_debug >= 1:
            l_msg = "Convert_pim - {0:}".format(PrintBytes(l_string))
            LOG.debug(l_msg)
        return l_string

    def change_register_command(self, p_controller_obj, *p_args):
        l_cmd = bytearray(len(p_args))
        for l_ix in range(len(p_args)):
            l_cmd[0 + l_ix] = str(p_args[0][l_ix])
        l_cmd = self._calculate_checksum(l_cmd)
        l_cmd[1:] = l_cmd
        l_cmd[0] = CTL_T
        l_cmd.append(0x0d)
        self.queue_pim_command(p_controller_obj, l_cmd)

    def change_register_command_FORCE(self, p_controller_obj, *_p_args):
        l_xx = b'\x14\x37\x30\x30\x33\x38\x44\x0d'
        self.queue_pim_command(p_controller_obj, l_xx)
        pass


class UpbPimUtility(object):

    def _compose_command(self, p_controller_obj, _p_command, _p_device_id, *p_args):
        """Build the command.

        @param p_controller_obj: is the controller information.
        @param p_command: is the command
        @param p_device_id: Is the UPB address of the target.
        @param p_args: is the data for the command
        """
        l_hdr = bytearray(0 + len(p_args))
        # l_hdr[0] = 0x14
        for l_ix in range(len(p_args)):
            l_hdr[0 + l_ix] = p_args[l_ix]
        l_hdr = self._calculate_checksum(l_hdr)
        l_msg = "Ctl:{0:#02x}  ".format(l_hdr[0])
        if g_debug >= 1:
            LOG.debug('Compose Command - {0:}'.format(l_msg))
        self.queue_pim_command(p_controller_obj, l_hdr)


class DecodeResponses(object):

    def _next_char(self):
        try:
            self.l_hdr = self.l_message[0]
            self.l_message = self.l_message[1:]
            self.l_msg_len = self.l_msg_len - 1
        except IndexError:
            self.l_hdr = 0x00
            self.l_msg_len = 0

    def _get_rest(self):
        l_rest = self.l_hdr
        while self.l_hdr != 0x0d:
            self._next_char()
            l_rest += self.l_hdr
        return l_rest

    def _flushing(self):
        l_ret = 'Flushed: '
        while self.l_hdr != 0x0d and self.l_msg_len > 0:
            l_ret += "{0:#2x} ".format(self.l_hdr)
            self._next_char()
            print("Flushed {0:#2x} --- ".format(self.l_hdr))
        if g_debug >= 1:
            LOG.debug(l_ret)

    def _get_message_body(self, p_message):
        """
        A valid message begins with 'P' (0x50) and ends with \r (0x0D).
        While we have chars left in the message, find the Start of the message.
        """
        if len(p_message) < 1:
            return False
        print('Message = {0:}'.format(PrintBytes(p_message)))
        return True


    def decode_response(self, p_controller_obj):
        """A response message starts with a 'P' (0x50) and ends with a '\r' (0x0D).
        """
        self.m_controller_obj = p_controller_obj
        if self._get_message_body(p_controller_obj._Message) == False:
            return
        l_message = p_controller_obj._Message
        l_hdr = l_message[0]
        l_msg_len = len(l_message)
        l_message = l_message[1:]
        if l_msg_len < 1:
            return
        while l_msg_len > 0:
            self._next_char()  # Get the starting char - must be 'P' (0x50)
            if l_hdr != 0x50:
                l_msg = "UPB_Pim.decode_response() - Did not find valid message start 'P'(0x50)  - ERROR! char was {0:#x} - Flushing till next 0x0D".format(self.l_hdr)
                LOG.warning(l_msg)
                self._flushing()
                continue
            #
            self._next_char()  # drop the 0x50 char
            if l_hdr == 0x41:  # 'A'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was accepted")
            elif l_hdr == 0x42:  # 'B'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was rejected because device is busy.")
            elif l_hdr == 0x45:  # 'E'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was rejected with a command error.")
            elif l_hdr == 0x4B:  # 'K'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'K' (0x4b) - ACK pulse also received.")
            elif l_hdr == 0x4E:  # 'N'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'N' (0x4E) - No ACK pulse received from device.")
            elif l_hdr == 0x52:  # 'R'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'R' (0x52) - Register report recieved")
                self._get_rest()
            elif l_hdr == 0x55:  # 'U'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'U' (0x55) - Message report received.")
                self._get_rest()
            else:
                LOG.error("UPB_Pim.decode_response() found unknown code {0:#x} {1:}".format(self.l_hdr, PrintBytes(self.l_message)))
            self._next_char()  # Drop the 0x0d char


class PimDriverInterface(DecodeResponses):

    def driver_loop_start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.dequeue_and_send(p_controller_obj)
        self.receive_loop(p_controller_obj)

    def queue_pim_command(self, p_controller_obj, p_command):
        if g_debug >= 1:
            l_msg = "Queue_pim_command {0:}".format(PrintBytes(p_command))
            LOG.debug(l_msg)
        p_controller_obj._Queue.put(p_command)

    def dequeue_and_send(self, p_controller_obj):
        self.m_pyhouse_obj.Twisted.Reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send, p_controller_obj)
        try:
            l_command = p_controller_obj._Queue.get(False)
        except  Queue.Empty:
            return
        if p_controller_obj._DriverAPI != None:
            # l_send = self._convert_pim(l_command)
            l_send = l_command
            p_controller_obj._DriverAPI.Write(l_send)
            if g_debug >= 1:
                l_msg = 'Sent to controller:{0:}, Message: {1:} '.format(p_controller_obj.Name, PrintBytes(l_send))
                LOG.debug(l_msg)

    def receive_loop(self, p_controller_obj):
        """Periodically, get the current RX data from the driver.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop, p_controller_obj)
        if p_controller_obj._DriverAPI != None:
            l_msg = p_controller_obj._DriverAPI.fetch_read_data(p_controller_obj)
            if len(l_msg) == 0:
                return
            self.decode_response(p_controller_obj)


class CreateCommands(UpbPimUtility, PimDriverInterface, BuildCommand):
    """
    """

    def set_register_value(self, p_controller_obj, p_register, p_values):
        """Set one of the device's registers.
        """
        if g_debug >= 1:
            LOG.debug("Setting register {0:#0x} to value {1:}".format(p_register, p_values))
        # self._compose_command(p_controller_obj, pim_commands['set_register_value'], int(p_controller_obj.UPBAddress), int(p_register), p_values[0])
        self.change_register_command_FORCE(p_controller_obj, p_values)
        pass

    def set_pim_mode(self):
        """
        Send a write register 70 to set PIM mode
        Command to be sent is <17> 70 03 8D <0D>
        """
        l_val = bytearray(1)
        l_val[0] = 0x03
        if g_debug >= 1:
            LOG.debug("Setting Pim Mode - Register {0:#X} to value {1:}".format(0x70, l_val))
        self.set_register_value(0xFF, 0x70, l_val)


class UpbPimAPI(CreateCommands):

    def _load_driver(self, p_controller_obj):
        if p_controller_obj.InterfaceType.lower() == 'serial':
            from Modules.drivers import Driver_Serial
            l_driver = Driver_Serial.API()
        elif p_controller_obj.InterfaceType.lower() == 'ethernet':
            from Modules.drivers import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif p_controller_obj.InterfaceType.lower() == 'usb':
            from Modules.drivers import Driver_USB
            l_driver = Driver_USB.API()
        return l_driver

    def _initilaize_pim(self, p_controller_obj):
        l_pim = UPBData()
        l_pim.InterfaceType = p_controller_obj.InterfaceType
        l_pim.Name = p_controller_obj.Name
        l_pim.UPBAddress = p_controller_obj.UPBAddress
        l_pim.UPBPassword = p_controller_obj.UPBPassword
        l_pim.UPBNetworkID = p_controller_obj.UPBNetworkID
        LOG.info('Found UPB PIM named: {0:}, Type={1:}'.format(l_pim.Name, l_pim.InterfaceType))
        return l_pim

    def start_controller(self, p_pyhouse_obj, p_controller_obj):
        """
        """
        p_controller_obj._Queue = Queue.Queue(300)
        if g_debug >= 1:
            LOG.debug("UPB_PIM.start_controller() - ControllerFamily:{0:}, InterfaceType:{1:}".format(
                        p_controller_obj.ControllerFamily, p_controller_obj.InterfaceType))
        l_pim = self._initilaize_pim(p_controller_obj)
        l_driver = self._load_driver(p_controller_obj)
        l_driver.Start(p_pyhouse_obj, p_controller_obj)
        p_pyhouse_obj.House.OBJs.Controllers[p_controller_obj.Key]._DriverAPI = l_driver
        l_pim._DriverAPI = l_driver
        self.set_register_value(p_controller_obj, 0x70, [0x03])
        return True

    def get_response(self):
        pass


class API(UpbPimAPI):
    m_pyhouse_obj = None
    m_controller_obj = None

    def __init__(self):
        LOG.info('Initialized.')

    def Start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        if self.start_controller(p_pyhouse_obj, p_controller_obj):
            LOG.info('Starting driver loop')
            self.driver_loop_start(p_pyhouse_obj, p_controller_obj)
            return True
        return False

    def Stop(self, p_controller_obj):
        pass

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        for l_obj in self.m_house_obj.Lights.itervalues():
            if l_obj.Active == False:
                continue
            l_name = p_light_obj.Name
            if l_obj.Name == l_name:
                l_id = self._get_id_from_name(l_name)
                LOG.info('Change light {0:} to Level {1:}'.format(l_name, p_level))
                self._compose_command(self.m_controller_obj, pim_commands['goto'], l_id, p_level, 0x01)
                return

# ## END DBK
