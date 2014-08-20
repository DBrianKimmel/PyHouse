"""
Modules/families/UPB/UPB_Pim.py

@name: PyHouse/src/Modules/families/UPB/Device_UPB.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 27, 2011
@summary: This module is for communicating with UPB controllers.

/srv/backup/home/briank/svn/smarthouse/trunk/Modules/parts/upb/usbhidserial.cpp
"""

# Import system type stuff
import Queue

# Import PyMh files
from Modules.Families.UPB.UPB_data import UPBData
from Modules.Utilities.tools import PrintBytes
from Modules.Utilities import pyh_log

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
RECEIVE_TIMEOUT = 0.9  # this is for fetching data in the RX buffer


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


class UpbPimData(object):
    def __init__(self):
        self.Name = 'Undefined Upb Pim'
        self.InterfaceType = ''  # Serial | USB | Ethernet
        self.UPBAddress = 0
        self.UPBPassword = 0
        self.UPBNetworkID = 0
        #
        self._Message = ''
        self._Queue = None
        self._DriverAPI = None  # InterfaceType API() - Serial, USB etc.


class BuildCommand(object):
    """
    This class will take a command bytearray and convert it to a bytearray for sending.

    Write register commands:
    The command for changing register 70's value to 03 is  ==> 70 03.
    First we add a checksum (8D in this case) to the bytearray ==> 70 03 8D.
    next 70 03 8D is converted to 37 30 30 33 38 44 by converting each nibble to an ascii hex value.
    Finally the command becomes 14 37 30 30 33 38 44 0D and is queued for sending
    """

    def _nibble_to_hex(self, p_nibble):
        """
        Take the low order nibble and convert it to a single byte that is the ASCII code for the nibble.
        0x01 ==> 0x31 ('1')
        @return: an int
        """
        l_ret = 0x30 + p_nibble
        if l_ret > 0x39:
            l_ret += 0x07
        l_ret = chr(l_ret)
        return ord(l_ret)

    def _byte_to_2chars(self, p_byte):
        """
        Take a single byte and return 2 bytes that are the ascii hex equivalent.

        0x12 ==> 0x3132 ('12')

        @return: a 2 byte array of ints that are ASCII encoded.
        """
        l_ret = bytearray(2)
        l_ret[0] = self._nibble_to_hex(p_byte / 16)
        l_ret [1] = self._nibble_to_hex(p_byte % 16)
        return l_ret

    def _calculate_checksum(self, p_ba):
        """Take a ByteArray of arbitrary length and return a byte array with the checksum appended to the original.

        b'\x70\x03' ==> b'\x70\x03\x8D'
        @return: a bytearray with the checksum byte appended
        """
        l_out = bytearray(0)
        l_cs = 0
        for l_ix in range(len(p_ba)):
            try:
                l_byte = ord(p_ba[l_ix])
            except:
                l_byte = p_ba[l_ix]
            l_cs = (l_cs + l_byte) % 256
            l_out.append(l_byte)
        l_out.append(int(256 - l_cs))
        return l_out

    def _assemble_regwrite(self, p_reg, p_args):
        """Take the command and the args and make a ByteArray with the checksum appended

        @param p_reg: is the register number where we will start writing.
        @param p_args: is the one or more values that we will write into the registers
        @return: the ByteArray body of the register write command
        """
        l_cmd = bytearray(len(p_args) + 1)
        l_cmd[0] = p_reg
        for l_ix in range(len(p_args)):
            l_cmd[1 + l_ix] = p_args[l_ix]
        l_cmd = self._calculate_checksum(l_cmd)
        return l_cmd

    def _convert_pim(self, p_array):
        """Take a command ByteArray and convert it for the serial interface of the pim.

        I think this means taking each nibble of the command and converting it to an ASCII byte.

        """
        l_ret = bytearray(0)
        for l_byte in p_array:
            l_str = self._byte_to_2chars(l_byte)
            l_ret.append(l_str[0])
            l_ret.append(l_str[1])
        if g_debug >= 1:
            LOG.debug("Convert_pim - {0:}".format(PrintBytes(l_ret)))
        return l_ret

    def _create_packet_header(self):
        l_ph = bytearray(5)
        l_ph[0] = 0
        l_ph[1] = 0
        l_ph[2] = self.m_pim.NetworkID
        l_ph[3] = self.m_pim.UPBAddress
        l_ph[4] = 0xff
        return l_ph

    def _queue_pim_command(self, p_controller_obj, p_command):
        if g_debug >= 1:
            l_msg = "Queue_pim_command {0:}".format(PrintBytes(p_command))
            LOG.debug(l_msg)
        p_controller_obj._Queue.put(p_command)

    def write_register_command(self, p_controller_obj, p_reg, p_args):
        """Take a starting register and one or more values and write them into the controller.
        Use a 0x14 header to create the command
        """
        l_cmd = self._assemble_regwrite(p_reg, p_args)
        l_cmd[1:] = self._convert_pim(l_cmd)
        l_cmd[0] = CTL_W
        l_cmd.append(0x0d)
        self._queue_pim_command(p_controller_obj, l_cmd)
        return l_cmd

    def  write_pim_command(self, p_controller_obj, _p_command, _p_device_id, *p_args):
        """Send a command to some UPB device thru the controller
        """
        pass


class UpbPimUtility(object):

    def _compose_command(self, _p_controller_obj, _p_command, _p_device_id, *p_args):
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
        # self.queue_pim_command(p_controller_obj, l_hdr)



class DecodeResponses(object):

    def _get_rest(self, p_message):
        l_rest = p_message[2:]
        return l_rest

    def _extract_one_message(self, p_controller_obj):
        """Valid messages start with a 'P' (0x50) and end with a NewLine (0x0dD).
        Remove any leading Junk characters
        Skip over any 0xFx characters as they are a USB HID length of data byte.
        Find the next Newline - If none we do not have a command so leave things in the _Message buffer.
        """
        l_start = p_controller_obj._Message.find('P')
        l_end = p_controller_obj._Message.find('\r')
        if l_end < 0:
            return ''  # Not a complete message yet.
        if l_start > 0:
            LOG.warning('Decoding result - discarding leading junk {0:}'.format(PrintBytes(p_controller_obj._Message[0:l_start])))
            p_controller_obj._Message = p_controller_obj._Message[l_start:]
            l_start = 0
            l_end = p_controller_obj._Message.find('\r')
            if l_end < 0:
                return ''  # Not a complete message yet.
        l_message = p_controller_obj._Message[l_start:l_end]
        p_controller_obj._Message = p_controller_obj._Message[l_end + 1:]
        LOG.debug('Extracted message {0:}'.format(PrintBytes(l_message)))
        return l_message

    def _dispatch_decode(self, p_message):
        """
        Dispatch to the various message received methods

        See Page 12 of - UPB Powerline Interface Module (PIM) Description Ver 1.6
        """
        l_hdr = p_message[1]
        if l_hdr == 0x41:  # 'A'
            self._decode_A()
        elif l_hdr == 0x42:  # 'B'
            self._decode_B()
        elif l_hdr == 0x45:  # 'E'
            self._decode_E()
        elif l_hdr == 0x4B:  # 'K'
            self._decode_K()
        elif l_hdr == 0x4E:  # 'N'
            self._decode_N()
        elif l_hdr == 0x52:  # 'R'
            self._decode_R()
        elif l_hdr == 0x55:  # 'U'
            self._decode_U()
        else:
            LOG.error("UPB_Pim.decode_response() found unknown code {0:#x} {1:}".format(l_hdr, PrintBytes(p_message)))

    def decode_response(self, p_controller_obj):
        """A response message starts with a 'P' (0x50) and ends with a '\r' (0x0D).
        """
        LOG.debug('DecodeResponse A - {0:}'.format(PrintBytes(p_controller_obj._Message)))
        l_message = self._extract_one_message(p_controller_obj)
        LOG.debug('DecodeResponse B - {0:}'.format(PrintBytes(l_message)))
        if len(l_message) == 0:
            return
        self._dispatch_decode(l_message)
        self.decode_response(p_controller_obj)

    def _decode_A(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim - Previous command was accepted")

    def _decode_B(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim - Previous command was rejected because device is busy.")

    def _decode_E(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim - Previous command was rejected with a command error.")

    def _decode_K(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim.decode_response() found 'K' (0x4b) - ACK pulse also received.")

    def _decode_N(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim.decode_response() found 'N' (0x4E) - No ACK pulse received from device.")

    def _decode_R(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim.decode_response() found 'R' (0x52) - Register report received")
        self._get_rest()

    def _decode_U(self):
        if g_debug >= 2:
            LOG.error("UPB_Pim.decode_response() found 'U' (0x55) - Message report received.")
        self._get_rest()


class PimDriverInterface(DecodeResponses):

    def driver_loop_start(self, p_pyhouse_obj, p_controller_obj):
        LOG.info('Start driver loop')
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Sending first command')
        self.dequeue_and_send(p_controller_obj)
        LOG.info('About to start RX loop')
        self.receive_loop(p_controller_obj)

    def XXXqueue_pim_command(self, p_controller_obj, p_command):
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
            if g_debug >= 1:
                LOG.debug('Sending to controller:{0:}, Message: {1:} '.format(p_controller_obj.Name, PrintBytes(l_command)))
            p_controller_obj._DriverAPI.Write(l_command)

    def receive_loop(self, p_controller_obj):
        """Periodically, get the current RX data from the driver.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop, p_controller_obj)
        if p_controller_obj._DriverAPI != None:
            l_msg = p_controller_obj._DriverAPI.Read()
            if len(l_msg) == 0:
                return
            if g_debug >= 2:
                LOG.debug('Fetched message  {0:}'.format(PrintBytes(l_msg)))
            p_controller_obj._Message += l_msg
            self.decode_response(p_controller_obj)
        else:
            if g_debug >= 1:
                LOG.info('No driver defined ')


class CreateCommands(UpbPimUtility, PimDriverInterface, BuildCommand):
    """
    """

    def set_register_value(self, p_controller_obj, p_register, p_values):
        """Set one of the device's registers.
        """
        if g_debug >= 1:
            LOG.debug("Setting register {0:#0x} to value {1:}".format(p_register, p_values))
        self.write_register_command(p_controller_obj, p_register, p_values)
        pass

    def set_pim_mode(self):
        """
        Set the PIM operating mode:

        Page 6 of UPB Powerline Interface Module (PIM) Description Version 1.6

        The PIM mode register is 0x70

        Bit 0 (lsb) set to 1 is "No Idles Sent"
        Bit 1 set to 1 puts the PIM into "Message Mode"

        Send a write register 70 to set PIM mode
        Command to be sent is <17> 70 03 8D <0D>
        """
        l_val = bytearray(1)
        l_val[0] = 0x03
        self.set_register_value(0xFF, 0x70, l_val)

    def null_command(self, p_controller_obj):
        self.write_pim_command(p_controller_obj, pim_commands['null'], '0xFF')
        pass


class UpbPimAPI(CreateCommands):

    def _load_driver(self, p_controller_obj):
        """
        Select a driver depending on the controller's interface type.

        """
        l_driver = None
        if p_controller_obj.InterfaceType.lower() == 'serial':
            from Modules.Drivers.Serial import Driver_Serial
            l_driver = Driver_Serial.API()
        elif p_controller_obj.InterfaceType.lower() == 'ethernet':
            from Modules.Drivers.Ethernet import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif p_controller_obj.InterfaceType.lower() == 'usb':
            from Modules.Drivers.USB import Driver_USB
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
            LOG.debug("start_controller() - InterfaceType:{0:}".format(p_controller_obj.InterfaceType))
        self.m_pim = self._initilaize_pim(p_controller_obj)
        l_driver = self._load_driver(p_controller_obj)
        l_driver.Start(p_pyhouse_obj, p_controller_obj)
        p_pyhouse_obj.House.OBJs.Controllers[p_controller_obj.Key]._DriverAPI = l_driver
        self.m_pim._DriverAPI = l_driver
        self.set_register_value(p_controller_obj, 0x70, [0x03])
        self.null_command(p_controller_obj)
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


"""
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
# ## END DBK
