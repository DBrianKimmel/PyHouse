#!/usr/bin/env python

"""
src/families/UPB/UPB_Pim.py

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright (c) 2010-2014 by D. Brian Kimmel

@license: MIT License

@summary: Handle the controller component of the lighting system.


/srv/backup/home/briank/svn/smarthouse/trunk/src/parts/upb/usbhidserial.cpp

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
from twisted.internet import reactor

# Import PyMh files
import Device_UPB
from src.utils.tools import PrintBytes
from src.utils import pyh_log

g_debug = 2
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.UPB_PIM     ')

callLater = reactor.callLater


# UPB Control Word
# Page 15
LINK_PKT = 0x80
LOW_REQ = 0x02

ACK_REQ = 0x10
ACK_ID = 0x20
ACK_MSG = 0x40

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for fetching data in the rx buffer


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


# Controller_Data = Device_UPB.Controller_Data


class PimData(object):
    """Locally held data about each of the PIM controllers we find.
    """

    def __init__(self):
        self.Interface = None
        self.Name = None
        self.NetworkID = 0
        self.Password = None
        self.UnitID = 0xFF


class UpbPimUtility(object):

    def _calculate_checksum(self, p_msg):
        l_out = bytearray(0)
        l_cs = 0
        for l_ix in range(len(p_msg)):
            l_byte = p_msg[l_ix]
            l_cs = (l_cs + l_byte) % 256
            l_out.append(l_byte)
        l_out.append(int(256 - l_cs))
        if g_debug >= 1:
            LOG.debug("Calculate checksum - {0:}".format(PrintBytes(l_out)))
        return l_out

    def _compose_command(self, p_controller_obj, _p_command, _p_device_id, *p_args):
        """Build the command for each controller found.
        """
        l_hdr = bytearray(0 + len(p_args))
        # l_hdr[0] = 0x14
        for l_ix in range(len(p_args)):
            l_hdr[0 + l_ix] = p_args[l_ix]
        l_hdr = self._calculate_checksum(l_hdr)
        l_msg = "Ctl:{0:#02X}  ".format(l_hdr[0])
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

    def decode_response(self, p_message):
        """A message starts with a 'P' (0x50) and ends with a '\r' (0x0D).
        """
        if len(p_message) < 1:
            return
        self.l_message = p_message
        # Get the length which seems to be x in 0xFx first byte
        # self.l_msg_len = p_message[0] & 0x0F
        # self._next_char()
        self.l_hdr = self.l_message[0]
        self.l_msg_len = len(self.l_message)
        self.l_message = self.l_message[1:]
        # All PIM response messages begin with 'P' which is 0x50
        if self.l_msg_len < 1:
            return
        while self.l_msg_len > 0:
            self._next_char()  # Get the starting char - must be 'P' (0x50)
            if self.l_hdr != 0x50:
                l_msg = "UPB_Pim.decode_response() - Did not find valid message start 'P'(0x50)  - ERROR! char was {0:#x} - Flushing till next 0x0D".format(self.l_hdr)
                LOG.warning(l_msg)
                self._flushing()
                continue
            #
            self._next_char()  # drop the 0x50 char
            if self.l_hdr == 0x41:  # 'A'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was accepted")
            elif self.l_hdr == 0x42:  # 'B'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was rejected because device is busy.")
            elif self.l_hdr == 0x45:  # 'E'
                if g_debug >= 2:
                    LOG.error("UPB_Pim - Previous command was rejected with a command error.")
            elif self.l_hdr == 0x4B:  # 'K'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'K' (0x4b) - ACK pulse also received.")
            elif self.l_hdr == 0x4E:  # 'N'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'N' (0x4E) - No ACK pulse received from device.")
            elif self.l_hdr == 0x52:  # 'R'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'R' (0x52) - Register report recieved")
                self._get_rest()
            elif self.l_hdr == 0x55:  # 'U'
                if g_debug >= 2:
                    LOG.error("UPB_Pim.decode_response() found 'U' (0x55) - Message report received.")
                self._get_rest()
            else:
                LOG.error("UPB_Pim.decode_response() found unknown code {0:#x} {1:}".format(self.l_hdr, PrintBytes(self.l_message)))
            self._next_char()  # Drop the 0x0d char

""" int PIMMain::decodeResponse( QByteArray& k_msg, QByteArray& k_msgRet ) {
    QString l_str = messageToString( k_msg );
    // All pIM response messages begin with 'P' which is 0x50
    if ( l_response[0] != (char)0x50 ) {
        DEBUG( 1, "decodeResponse did not find valid message 1 - ERROR! char was " << (int)l_response[0] );
        l_response.remove( 0, 1 );
        l_len--;
        if ( l_len < 1 ) return -1;
    }
    while ( l_len > 0 ) {
        if ( l_response[0] == (char) 0x0D ) {
            l_response.remove( 0, 1 );
            l_len--;
            //l_ret = -1;
            continue;
        }
        if ( l_response[0] != (char)0x50 ) {
            DEBUG( 1, "decodeResponse did not find valid message 2 - ERROR! char was " << (int)l_response[0] );
            l_response.remove( 0, 1 );
            l_len--;
            l_ret = -1;
            continue;
        }
        switch( l_response[1] ) {
            case 0x41:      // 'A'
                DEBUG( 3, "... A - Message accepted." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x0001;
                break;
            case 0x45:      // 'E'
                DEBUG( -3, "... E - Rejected prev cmd because it contained an error." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8001;
                break;

            case 0x4B:      // 'K'
                DEBUG( 3, "... K - Ack pulse was also recieved." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x0002;
                break;
            case 0x4E:      // 'N'
                DEBUG( -3, "... N - NO ack pulse was recieved from device." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8002;
                break;

            case 0x42:      // 'B'
                DEBUG( -3, "... B - Rejected prev cmd because PIM is busy." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8004;
                break;

            case 0x52:      // 'R'
                // get rid of 'PR'
                l_response.remove( 0, 2 ); l_len -= 2;
                // get register #
                l_reg =  l_response.left( 2 ); l_response.remove( 0, 2 ); l_len -= 2;
                // we now have the registers values encoded as hex nibbles
                while ( l_response[0] != (char)0x0d ) {
                    k_msgRet.append( l_response[0] );
                    l_response.remove( 0, 1 );
                    l_len--;
                }
                DEBUG( 3, "... R - Register report recieved - Register=" << l_reg << " " << k_msgRet );
                l_ret |= 0x0010;
                break;

            case 0x55:      // 'U'
                l_response.remove( 0, 2 );
                l_len -= 2;
                l_reg =  l_response.left( 2 );
                l_response.remove( 0, 2 );
                l_len -= 2;
                while ( l_response[0] != (char)0x0d ) {
                    k_msgRet.append( l_response[0] );
                    l_response.remove( 0, 1 );
                    l_len--;
                }
                l_len--;
                DEBUG( -3, "... U - Message Report recieved - len=" << l_reg << "  " << k_msgRet << " Len-" << l_len );
                l_ret |= 0x0020;
                break;

            default:
                DEBUG( 0, "... Unhandled return message. len=" << l_len << " " << l_response );
                l_len--;
                l_response.remove( 0, 1 );
                l_ret |= 0x8100;
        }
    }
    return l_ret;
}
"""


class PimDriverInterface(DecodeResponses):

    def _convert_pim(self, p_array):
        l_string = chr(0x14)
        for l_byte in p_array:
            l_char = "{0:02X}".format(l_byte)
            # l_char = chr(l_byte)
            l_string += l_char
        l_string += chr(0x0D)
        if g_debug >= 1:
            l_msg = "Convert_pim - {0:}".format(PrintBytes(l_string))
            LOG.debug(l_msg)
        return l_string

    def driver_loop_start(self, p_controller_obj):
        self.dequeue_and_send(p_controller_obj)
        self.receive_loop(p_controller_obj)

    def queue_pim_command(self, p_controller_obj, p_command):
        if g_debug >= 1:
            l_msg = "Queue_pim_command {0:}".format(PrintBytes(p_command))
            LOG.debug(l_msg)
        p_controller_obj._Queue.put(p_command)

    def dequeue_and_send(self, p_controller_obj):
        callLater(SEND_TIMEOUT, self.dequeue_and_send, p_controller_obj)
        try:
            l_command = p_controller_obj._Queue.get(False)
        except  Queue.Empty:
            return
        if p_controller_obj._DriverAPI != None:
            l_send = self._convert_pim(l_command)
            # l_send = l_command
            p_controller_obj._DriverAPI.Write(l_send)
            if g_debug >= 1:
                l_msg = 'Sent to controller:{0:}, Message: {1:} '.format(p_controller_obj.Name, PrintBytes(l_send))
                LOG.debug(l_msg)

    def receive_loop(self, p_controller_obj):
        callLater(RECEIVE_TIMEOUT, self.receive_loop, p_controller_obj)
        if p_controller_obj._DriverAPI != None:
            l_msg = p_controller_obj._DriverAPI.fetch_read_data(p_controller_obj)
            if len(l_msg) == 0:
            # if l_msg[0] == 0xF0:
                return
            self.decode_response(l_msg)


class CreateCommands(UpbPimUtility, PimDriverInterface):
    """
    """

    def set_register_value(self, p_controller_obj, p_register, p_values):
        """Set one of the device's registers.
        """
        if g_debug >= 1:
            LOG.debug("Setting register {0:#0X} to value {1:}".format(p_register, p_values))
        self._compose_command(p_controller_obj, pim_commands['set_register_value'], int(p_controller_obj.UnitID), int(p_register), p_values[0])
        pass

    def set_pim_mode(self):
        # Send a write register 70 to set PIM mode
        # Command is <17> 70 03 8D <0D>
        l_val = bytearray(1)
        l_val[0] = 0x03
        if g_debug >= 1:
            LOG.debug("Setting Pim Mode - Register {0:#X} to value {1:}".format(0x70, l_val))
        self.set_register_value(0xFF, 0x70, l_val)


class LightingAPI(Device_UPB.LightingAPI, CreateCommands):
    pass


class UpbPimAPI(LightingAPI):

    def start_controller(self, p_house_obj, p_controller_obj):
        """Find and initialize the UPB PIM type controllers.

        skip all NON UPB controllers.
        Also skip controllers that are not active.

        Set up the controller and create links to it.
        Initialize the controller
        Initialize any interface special requirements.
        """
        self.m_controller_obj = p_controller_obj
        self.m_controller_obj._Queue = Queue.Queue(300)
        if self.m_controller_obj.Family.lower() != 'upb':
            return False
        if self.m_controller_obj.Active != True:
            return False
        if g_debug >= 1:
            LOG.debug("UPB_PIM.start_controller() - Family:{0:}, Interface:{1:}, Active:{2:}".format(self.m_controller_obj.Family, self.m_controller_obj.Interface, self.m_controller_obj.Active))
        l_key = self.m_controller_obj.Key
        l_pim = PimData()
        l_pim.Interface = self.m_controller_obj.Interface
        l_pim.Name = self.m_controller_obj.Name
        l_pim.NetworkID = int(self.m_controller_obj.NetworkID, 0)
        l_pim.Password = self.m_controller_obj.Password
        l_pim.UnitID = int(self.m_controller_obj.UnitID, 0)
        LOG.info('Found UPB PIM named: {0:}, Type={1:}'.format(l_pim.Name, l_pim.Interface))
        if self.m_controller_obj.Interface.lower() == 'serial':
            from drivers import Driver_Serial
            l_driver = Driver_Serial.API()
        elif self.m_controller_obj.Interface.lower() == 'ethernet':
            from drivers import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif self.m_controller_obj.Interface.lower() == 'usb':
            # from drivers import Driver_USB_17DD_5500
            from src.drivers import Driver_USB
            # l_driver = Driver_USB_17DD_5500.API()
            l_driver = Driver_USB.API()
        l_driver.Start(self.m_controller_obj)
        p_house_obj.Controllers[l_key]._DriverAPI = l_driver
        l_pim._DriverAPI = l_driver
        self.set_register_value(p_controller_obj, 0x70, [0x03])
        return True

    def get_response(self):
        pass


class API(UpbPimAPI):

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        LOG.info('Initialized.')

    def Start(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj
        LOG.info('Start House:{0:}, Controller:{1:}.'.format(self.m_house_obj.Name, self.m_controller_obj.Name))
        self.start_controller(self.m_house_obj, self.m_controller_obj)
        self.driver_loop_start(p_controller_obj)
        return True

    def Stop(self, p_controller_obj):
        pass

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        for l_obj in self.m_house_obj.Lights.itervalues():
            if l_obj.Family != 'UPB':
                continue
            if l_obj.Active == False:
                continue
            l_name = p_light_obj.Name
            if l_obj.Name == l_name:
                l_id = self._get_id_from_name(l_name)
                LOG.info('Change light {0:} to Level {1:}'.format(l_name, p_level))
                self._compose_command(self.m_controller_obj, pim_commands['goto'], l_id, p_level, 0x01)
                return

# ## END DBK
