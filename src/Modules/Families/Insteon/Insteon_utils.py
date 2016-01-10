"""
-*- test-case-name: PyHouse/src/Modules/Families/Insteon/test/test_Insteon_utils.py -*-

@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for Insteon conversion routines.

This is a bunch of routines to deal with Insteon devices.
Some convert things like addresses '14.22.A5' to a int for ease of handling.

"""

#  Import system type stuff

#  Import PyMh files
from Modules.Core import conversions
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Families.Insteon.Insteon_constants import MESSAGE_LENGTH, NAK
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.tools import PrintBytes
from Modules.Core.data_objects import DeviceData
from Modules.Utilities import device_tools

LOG = Logger.getLogger('PyHouse.Insteon_Utils  ')


class Util(object):

    @staticmethod
    def int2message(p_int, p_message, p_index = 3):
        """Place an Insteon address (int internally) into a message at a given offset.
        The message must exist and be long enough to include a 3 byte area for the address.
        """
        if p_int > 16777215 or p_int < 0:
            l_msg = 'ERROR - Insteon_utils - trying to convert {} to message byte string.'.format(p_int)
            LOG.error(l_msg)
            p_int = 0xBADBAD
        l_ix = 256 * 256
        l_int = p_int
        while l_ix > 0:
            p_message[p_index], l_int = divmod(l_int, l_ix)
            l_ix = l_ix / 256
            p_index += 1
        return p_message

    @staticmethod
    def message2int(p_message):
        """Extract the address (3 bytes) from a response message.
        The message is a byte array returned from the PLM.
        Return a 24 bit int that is the address.
        """
        try:
            l_int0 = ord(p_message[0])
            l_int1 = ord(p_message[1])
            l_int2 = ord(p_message[2])
        except TypeError:
            l_int0 = int(p_message[0])
            l_int1 = int(p_message[1])
            l_int2 = int(p_message[2])
        l_int = ((l_int0 * 256) + l_int1) * 256 + l_int2
        return l_int

    @staticmethod
    def get_message_length(p_message):
        """ Get the documented length that the message is supposed to be.

        Use the message type byte to find out how long the response from the PLM is supposed to be.
        With asynchronous routines, we want to wait till the entire message is received before proceeding with its decoding.
        """
        l_id = p_message[1]
        try:
            l_message_length = MESSAGE_LENGTH[l_id]
        except KeyError:
            l_message_length = 1
        return l_message_length

    @staticmethod
    def get_json_data(p_obj, p_json):
        p_obj.DevCat = int(p_json['DevCat'])
        p_obj.GroupList = p_json['GroupList']
        p_obj.GroupNumber = p_json['GroupNumber']
        p_obj.InsteonAddress = int(p_json['InsteonAddress'])
        p_obj.ProductKey = int(p_json['ProductKey'])
        return p_obj


class Decode(object):

    @staticmethod
    def drop_first_byte(p_controller_obj):
        """The first byte is not legal, drop it and try again.
        Silently drop 1st byte if it is a NAK otherwise log it.
        """
        l_msg = "Found a leading char {:#x} - Rest. - {}".format(
                p_controller_obj._Message[0], PrintBytes(p_controller_obj._Message))
        if p_controller_obj._Message[0] != NAK:
            LOG.error(l_msg)
        try:
            p_controller_obj._Message = p_controller_obj._Message[1:]
        except IndexError:
            pass

    @staticmethod
    def _decode_message_flag(p_byte):
        """ Get the message flag and convert it to a description of the message.
        """
        def decode_message_type_flag(p_type):
            TYPE_X = ['Direct', 'Direct_ACK', 'AllCleanup', 'All_Cleanup_ACK', 'Broadcast', 'Direct_NAK', 'All_Broadcast', 'All_Cleanup_NAK']
            return TYPE_X[p_type] + ' Msg, '
        def decode_extended_flag(p_extended):
            TYPE_X = [' Standard Len,', ' Extended Len,']
            return TYPE_X[p_extended]
        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10)
        l_hops_left = (p_byte & 0x0C) >= 4
        l_max_hops = (p_byte & 0x03)
        l_ret = decode_message_type_flag(l_type)
        l_ret += decode_extended_flag(l_extended)
        l_ret += " HopsLeft:{:d}, Hops:{:d} ({:#X}); ".format(l_hops_left, l_max_hops, p_byte)
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
        """ Decode the DevCat and DevSubCat from a message.
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
        l_debug_msg = " DevCat={:#x}, ".format(l_devcat)
        return l_debug_msg

    @staticmethod
    def _find_addr_one_class(p_pyhouse_obj, p_class, p_addr):
        """
        Find the address of something Insteon.
        @param p_class: is an OBJ like p_pyhouse_obj.House.Lighting.Controllers that we will look thru to find the object.
        @param p_addr: is the address that we want to find.
        @return: the object that has the address.  None if not found
        """
        for l_obj in p_class.itervalues():
            if l_obj.DeviceFamily != 'Insteon':
                continue  #  ignore any non-Insteon devices in the class
            if l_obj.InsteonAddress == p_addr:
                return l_obj
        return None

    @staticmethod
    def find_address_all_classes(p_pyhouse_obj, p_address):
        """ This will search thru all object groups that an inseton device could be in.
        @return: the object that has the address or a dummy object if not found
        """
        l_ret = Decode._find_addr_one_class(p_pyhouse_obj, p_pyhouse_obj.House.Lighting.Lights, p_address)
        l_dotted = conversions.int2dotted_hex(p_address, 3)
        if l_ret == None:
            l_ret = Decode._find_addr_one_class(p_pyhouse_obj, p_pyhouse_obj.House.Lighting.Controllers, p_address)
        if l_ret == None:
            l_ret = Decode._find_addr_one_class(p_pyhouse_obj, p_pyhouse_obj.House.Lighting.Buttons, p_address)
        if l_ret == None:
            l_ret = Decode._find_addr_one_class(p_pyhouse_obj, p_pyhouse_obj.House.Hvac.Thermostats, p_address)
        #  Add additional classes in here
        if l_ret == None:
            LOG.info("WARNING - Address {} ({}) *NOT* found.".format(l_dotted, p_address))
            l_ret = DeviceData()
            device_tools.stuff_new_attrs(l_ret, InsteonData())  #  an empty new object
            l_ret.Name = '**NoName-' + l_dotted + '-**'
        return l_ret

    @staticmethod
    def get_obj_from_message(p_pyhouse_obj, p_message_addr):
        """ Here we have a message from the PLM.  Find out what device has that address.

        @param p_message_addr: is the address portion of the message byte array from the PLM we are extracting the Insteon address from.
        @param p_index: is the index of the first byte in the message.
                Various messages contain the address at different offsets.
        @return: The object that contains the address -or- a dummy object with noname in Name
        """
        l_address = Util.message2int(p_message_addr)  #  Extract the 3 byte address from the message and convert to an Int.
        if l_address < (256 * 256):  #  First byte zero ?
            l_dotted = str(l_address)
            l_device_obj = DeviceData()
            device_tools.stuff_new_attrs(l_device_obj, InsteonData())  #  an empty new object
            l_device_obj.Name = '**Group: ' + l_dotted + ' **'
        else:
            l_device_obj = Decode.find_address_all_classes(p_pyhouse_obj, l_address)
        return l_device_obj

#  ## END DBK
