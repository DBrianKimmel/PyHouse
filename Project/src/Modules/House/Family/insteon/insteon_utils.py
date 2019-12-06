"""
@name:      Modules/House/Family/insteon/insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for Insteon conversion routines.

This is a bunch of routines to deal with Insteon devices.
Some convert things like addresses '14.22.A5' to a int for ease of handling.

"""

__updated__ = '2019-12-04'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import CoreLightingData
from Modules.Core.Utilities.xml_tools import stuff_new_attrs
from Modules.House.Family.insteon.insteon_device import InsteonInformation
from Modules.House.Family.insteon.insteon_constants import \
    MESSAGE_LENGTH, \
    COMMAND_LENGTH, \
    PLM_COMMANDS, \
    STX

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Utils  ')


class InsteonQueueInformation:

    def __init__(self):
        self.Command = None
        self.Text = None


def create_command_message(p_command):
    """ Create a bytearray of the proper length
    """
    l_cmd = PLM_COMMANDS[p_command]
    l_command_bytes = bytearray(COMMAND_LENGTH[l_cmd])
    l_command_bytes[0] = STX
    l_command_bytes[1] = l_cmd
    return l_command_bytes


def queue_command(p_controller, p_command, p_text=None):
    """ Add the command into the queue
    @param p_command: is the bytestring to send to the controller
    @param p_text: is the text to log describing the command
    """
    l_entry = InsteonQueueInformation()
    l_entry.Command = p_command
    l_entry.Text = p_text
    p_controller._Queue.put(l_entry)


def get_message_length(p_message):
    """ Get the documented length that the message is supposed to be.

    Use the message type byte to find out how long the response from the PLM is supposed to be.
    With asynchronous routines, we want to wait till the entire message is received before proceeding with its decoding.
    """
    l_id = p_message[1]
    try:
        l_message_length = MESSAGE_LENGTH[l_id]
        if l_message_length < 8:
            return l_message_length
        if len(p_message) > 8:
            if p_message[8] & 0x10 > 0:
                l_message_length += 14
            pass
    except KeyError:
        l_message_length = 1
    return l_message_length


def decode_link_code(p_code):
    """
        LinkCode - 0=PLM is Responder, 1=PLM is Controller, FF=Deleted
    """
    l_msg = 'Unknown code {}'.format(p_code)
    if p_code == 0:
        l_msg = 'PLM=Responder'
    elif p_code == 1:
        l_msg = 'PLM=Controller'
    elif p_code == 0xFF:
        l_msg = 'Link Deleted'
    return l_msg


def decode_message_flag(p_byte):
    """ Get the message flag and convert it to a description of the message.
    """

    def decode_message_type_flag(p_type):
        MESSAGE_TYPE_X = ['Dir(SD)', 'Dir_ACK(SD-ACK)', 'AllCleanup(SC)', 'All_Cleanup_ACK(SC-ACK)', 'Brdcst(SB)', 'Direct_NAK(SD-NAK)', 'All_Brdcst(SA)', 'All_Cleanup_NAK(SC-NAK)']
        return MESSAGE_TYPE_X[p_type] + '-Msg, '

    def decode_extended_flag(p_extended):
        MESSAGE_LENGTH_X = [' Std-Len,', ' Ext-Len,']
        return MESSAGE_LENGTH_X[p_extended]

    l_type = (p_byte & 0xE0) >> 5
    l_extended = (p_byte & 0x10)
    l_hops_left = (p_byte & 0x0C) >= 4
    l_hops_max = (p_byte & 0x03)
    l_ret = decode_message_type_flag(l_type)
    l_ret += decode_extended_flag(l_extended)
    l_ret += " Hops:{:d}/{:d}({:#X})".format(l_hops_left, l_hops_max, p_byte)
    return l_ret


def update_insteon_obj(p_pyhouse_obj, p_insteon_obj):
    """ Given some insteon object feched from its insteon address, update the p_pyhouse_obj storage to reflect
    the new information gleaned from the insteon responses.
    """
    return
    l_ix = p_insteon_obj.Key
    try:
        if p_insteon_obj.DeviceType == 'Lighting' and p_insteon_obj.DeviceSubType == 'Button':
            p_pyhouse_obj.House.Lighting.Buttons[l_ix] = p_insteon_obj
        elif p_insteon_obj.DeviceType == 'Lighting' and p_insteon_obj.DeviceSubType == 'Controller':
            p_pyhouse_obj.House.Lighting.Controllers[l_ix] = p_insteon_obj
        elif p_insteon_obj.DeviceType == 'Lighting' and p_insteon_obj.DeviceSubType == 'Light':
            p_pyhouse_obj.House.Lighting.Lights[l_ix] = p_insteon_obj
        elif p_insteon_obj.DeviceType == 'Hvac':
            p_pyhouse_obj.House.Hvac.Thermostats[l_ix] = p_insteon_obj
        elif p_insteon_obj.DeviceType == 'Security' and p_insteon_obj.DeviceSubType == 'Thermostat':
            p_pyhouse_obj.House.Security.Garage_Doors[l_ix] = p_insteon_obj
        elif p_insteon_obj.DeviceType == 'Security' and p_insteon_obj.DeviceSubType == 'GarageDoorOpener':
            p_pyhouse_obj.House.Security.Motion_Detectors[l_ix] = p_insteon_obj
        else:
            LOG.warning('Unknown Insteon device to update: {}-{}'.format(p_insteon_obj.DeviceType, p_insteon_obj.DeviceSubType))
            # print(PrettyFormatAny.form(p_insteon_obj, 'InsteonUtil Unknown'))
    except AttributeError as e_err:
        LOG.error('ERROR {}'.format(e_err))


def insert_address_into_message(p_address, p_message, p_offset=2):
    """ Insert the insteon address into a byte stream message
    """
    # LOG.debug(PrettyFormatAny.form(p_address, 'Address', 190))
    l_ret = p_message
    p_message[p_offset] = int(p_address[0:2], 16)
    p_message[p_offset + 1] = int(p_address[3:5], 16)
    p_message[p_offset + 2] = int(p_address[6:8], 16)
    return  l_ret


def extract_address_from_message(p_message, offset=0):
    """
    """
    l_ret = '{:02X}.{:02X}.{:02X}'.format(p_message[offset], p_message[offset + 1], p_message[offset + 2])
    return l_ret


class Util:

    @staticmethod
    def get_json_data(p_obj, p_json):
        try:
            p_obj.DevCat = int(p_json['DevCat'])
            p_obj.GroupList = p_json['GroupList']
            p_obj.GroupNumber = p_json['GroupNumber']
            p_obj.InsteonAddress = int(p_json['InsteonAddress'])
            p_obj.ProductKey = int(p_json['ProductKey'])
        except KeyError:
            p_obj.DevCat = 0
            p_obj.GroupList = 'Bad insteon_utils.get_json_data()'
            p_obj.GroupNumber = 0
            p_obj.InsteonAddress = 1
            p_obj.ProductKey = 0
        return p_obj


class Decode:

    @staticmethod
    def decode_insteon_light_brightness(p_byte):
        return int(((p_byte + 2) * 100) / 256)

    @staticmethod
    def _decode_insteon_message_flag(p_byte):
        """ Get the message flag and convert it to a description of the message.
        See p 42(55) of 2009 developers guide.
        _________________________________
        | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
        | Type      | E | Hops  | Max   |

        @param b_byte: is a byte containing the flags
        @return: A string describing the flags

        Message Types  -  Bits 7(msb),6, 5  0xE0 >> 5
        000 = SD  = Direct Message
        001 = SDA = ACK of Direct Message
        010 = SC  = All Link Cleanup Message
        011 = SCA = ACK of All Link Cleanup Message
        100 = SB  = Broadcast Message
        101 = SDN = NAK of Direct Message
        110 = SA  = All Link Broadcast Message
        111 = SDN = NAK of All Link Cleanup Message

        """

        def decode_message_type_flag(p_type):
            MESSAGE_TYPE_X = ['SD', 'SDA', 'SC', 'SCA', 'SB', 'SDN', 'SA', 'SCN']
            return MESSAGE_TYPE_X[p_type] + ', '

        def decode_extended_flag(p_extended):
            MESSAGE_LENGTH_X = ['Std-Len', 'Ext-Len']
            return MESSAGE_LENGTH_X[p_extended] + ', '

        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10) >> 4
        l_hops_left = (p_byte & 0x0C) >> 2
        l_hops_max = (p_byte & 0x03)
        l_ret = decode_message_type_flag(l_type)
        l_ret += decode_extended_flag(l_extended)
        l_ret += "Hops:{:d}/{:d}({:#x})".format(l_hops_left, l_hops_max, p_byte)
        return l_ret

    @staticmethod
    def get_ack_nak(p_byte):
        if p_byte == 0x06:
            return 'ACK '
        elif p_byte == 0x15:
            return 'NAK '
        else:
            return "{:#02X} ".format(p_byte)

    @staticmethod
    def _devcat(p_message, p_obj):
        """ Decode the Dev-Cat and Dev-Sub-Cat from a message.
        @param p_message: is the message where the Devcat 2 bytes are located
            0x00    Generalized Controllers        ControLinc, RemoteLinc, SignaLinc, etc.
            0x01    Dimmable Lighting Control      Dimmable Light Switches, Dimmable Plug-In Modules
            0x02    Switched Lighting Control      Relay Switches, Relay Plug-In Modules
            0x03    Network Bridges                PowerLinc Controllers, TRex, Lonworks, ZigBee, etc.
            0x04    Irrigation Control             Irrigation Management, Sprinkler Controllers
            0x05    Climate Control                Heating, Air conditioning, Exhausts Fans, Ceiling Fans, Indoor Air Quality
            0x06    Pool and Spa Control           Pumps, Heaters, Chemicals
            0x07    Sensors and Actuators          Sensors, Contact Closures
            0x08    Home Entertainment             Audio/Video Equipment
            0x09    Energy Management              Electricity, Water, Gas Consumption, Leak Monitors
            0x0A    Built-In Appliance Control     White Goods, Brown Goods
            0x0B    Plumbing                       Faucets, Showers, Toilets
            0x0C    Communication                  Telephone System Controls, Intercoms
            0x0D    Computer Control               PC On/Off, UPS Control, App Activation, Remote Mouse, Keyboards
            0x0E    Window Coverings               Drapes, Blinds, Awnings
            0x0F    Access Control                 Automatic Doors, Gates, Windows, Locks
            0x10    Security, Health, Safety       Door and Window Sensors, Motion Sensors, Scales
            0x11    Surveillance                   Video Camera Control, Time-lapse Recorders, Security System Links
            0x12    Automotive                     Remote Starters, Car Alarms, Car Door Locks
            0x13    Pet Care                       Pet Feeders, Trackers
            0x14    Toys                           Model Trains, Robots
            0x15    Timekeeping                    Clocks, Alarms, Timers
            0x16    Holiday                        Christmas Lights, Displays
        """
        try:
            l_cat = ord(p_message[0])
            l_sub = ord(p_message[1])
        except TypeError:
            l_cat = int(p_message[0])
            l_sub = int(p_message[1])
        l_devcat = int(l_cat) * 256 + int(l_sub)
        p_obj.DevCat = l_devcat
        l_debug_msg = " Dev-Cat={:#x}, ".format(l_devcat)
        return l_debug_msg

    @staticmethod
    def _find_addr_one_class(p_class, p_addr):
        """
        Find the address of something Insteon.
        @param p_class: is an OBJ like p_pyhouse_obj.House.Lighting.Controllers that we will look thru to find the object.
        @param p_addr: is the address that we want to find.
        @return: the object that has the address.  None if not found in the given class.
        """
        # LOG.debug('Looking for address: {}'.format(p_addr))
        if p_class == None:
            return None
        try:
            for l_obj in p_class.values():
                # LOG.debug(PrettyFormatAny.form(l_obj, 'Object'))
                # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Object.Family'))
                if l_obj.Family.Name.lower() != 'insteon':
                    continue  #  ignore any non-Insteon devices in the class
                if l_obj.Family.Address == p_addr:
                    # LOG.debug(PrettyFormatAny.form(l_obj, 'Object'))
                    # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Object.Family'))
                    # LOG.debug('Found address "{}" in "{}" called "{}"'.format(p_addr, l_obj.DeviceSubType, l_obj.Name))
                    return l_obj
        except:
            pass
        return None

    @staticmethod
    def find_address_all_classes(p_pyhouse_obj, p_address):
        """ This will search thru all object groups that an inseton device could be in.
        @return: the object that has the address or a dummy object if not found
        """
        l_ret = None
        l_house = p_pyhouse_obj.House
        # LOG.debug(PrettyFormatAny.form(l_house, 'House'))
        if hasattr(l_house, 'Lighting'):
            # LOG.debug(PrettyFormatAny.form(l_house.Lighting, 'Lighting'))
            if l_ret == None and l_house.Lighting.Lights != None:
                l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Lighting.Lights, p_address)
            if l_ret == None and l_house.Lighting.Controllers != None:
                l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Lighting.Controllers, p_address)
            if l_ret == None and l_house.Lighting.Buttons != None:
                l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Lighting.Buttons, p_address)
            if l_ret == None and l_house.Lighting.Outlets != None:
                l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Lighting.Outlets, p_address)
        elif hasattr(l_house, 'Hvac') and hasattr(l_house.Hvac, 'Thermostats'):
            if l_ret == None and l_house.Hvac.Thermostats != None:
                l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Hvac.Thermostats, p_address)
        elif hasattr(l_house, 'Security'):
            if hasattr(l_house.Security, 'Garage_Doors'):
                if l_ret == None and l_house.Security.Garage_Doors != None:
                    l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Security.Garage_Doors, p_address)
            if hasattr(l_house.Security, 'Motion_Detectors'):
                if l_ret == None and l_house.Security.Motion_Detectors != None:
                    l_ret = Decode._find_addr_one_class(p_pyhouse_obj.House.Security.Motion_Detectors, p_address)
        #
        #  Add additional insteon classes in here
        #
        if l_ret == None:
            # LOG.debug(PrettyFormatAny.form(l_house, 'House'))
            LOG.debug(PrettyFormatAny.form(l_house.Security, 'Security'))
            LOG.debug(PrettyFormatAny.form(l_house.Security.Motion_Detectors, 'Security.M_D'))
            LOG.warning("WARNING - Address {} *NOT* found.".format(p_address))
            l_ret = CoreLightingData()
            stuff_new_attrs(l_ret, InsteonInformation())  #  an empty new object
            l_ret.Name = '**NoDevName-' + p_address + '-**'
        return l_ret

    def get_obj_from_message(self, p_pyhouse_obj, p_message_addr, offset=0):
        """ Here we have a message to or from an Insteon device.  Find out what device has that address.

        @param p_message_addr: is the address portion of the message byte array from the PLM we are extracting the Insteon address from.
        @return: The device object that contains the address -OR- a dummy object with noname in Name
        """
        # LOG.debug('Addr ')
        # Extract the 3 byte Insteon address from the message
        l_address = extract_address_from_message(p_message_addr, offset)
        if l_address.startswith('00'):  #  First byte zero ?
            l_dotted = str(l_address)
            l_device_obj = CoreLightingData()
            stuff_new_attrs(l_device_obj, InsteonInformation())  #  an empty new object
            l_device_obj.Name = '**Group: ' + l_dotted + ' **'
        else:
            l_device_obj = Decode.find_address_all_classes(p_pyhouse_obj, l_address)
        return l_device_obj

    def _x(self):
        PrettyFormatAny.form('', "hold")

#  ## END DBK
