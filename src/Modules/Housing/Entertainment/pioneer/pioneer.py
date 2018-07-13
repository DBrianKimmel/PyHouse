"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/pioneer.py -*-

@name:      src.Modules.Entertainment.pioneer
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Jul 10, 2016
@license:      MIT License
@summary:

http://www.mikepoulson.com/2011/06/programmatically-controlling-pioneer.html
https://dl.dropboxusercontent.com/u/3275573/2010%20USA%20AVR%20RS-232C%20%26%20IP%20Commands%20for%20CI.pdf



Basic Commands (more commands to come in another post):
?P
Is Device powered ON?
PWR0    Device is ON
PWR1    Device is OFF

PF    Power Device OFF
PO    Power Device ON

?M     Is Zone MAIN muted
MUT1    Zone is NOT Muted
MUT0    Zone is Muted

MO     Mute MAIN zone
MF     unMute MAIN zone

?V    Get Current Volume level
VOLxxx    Current volume level, xxx is 000-200
VOL121    -20.0db
VOL081    -40.0db
XXXVL    Set Volume Level to XXX (000 - 200)
001VL    Set Volume Level to -80.0db
081VL    Set Volume Level to -40.0db

VU        Set volume Up (822)
VD        Set volume Down (822)

?RGC    Get inputs on device (i think)
RGC111001002    *Unknown*

?RGBxx    Get inputs Name (related to above command), available inputs will change based on model
?RGB01    RGB010CD
?RGB02    RGB020TUNER
?RGB03    RGB030CD-R/TAPE

?F    Get current input (use ?RGB to get name)
FN19    Input 19
FN15    Input 15
XXFN    Set current input (XX = Input number)
XX    Input number
19FN    Set to input 19
15FN    Set to input 15

?BP    *UNKNOWN*
BPR1

?AP    *UNKNOWN*
APR1





Remote control your Pioneer VSX receiver over telnet
Posted by Raymond Julin on 15/07/2012



11
telnet <ip> VU<enter> #win!
I’m a hacker, developer and lazy guy.
So when I found myself in the kitchen cooking, just realizing that my Pioneer VSX 921 receiver was turned down too low I didn’t walk over
to turn it up or find the remote;
I instead remembered that it has a bad app for iOS, meaning that it accepts being controlled remote over the network.
A little bit of google searching and I found a plugin for an I-dont-know-what containing an XML with some Lua code (XML with code — yay),
 and also a very nice mapping table for commands the same code runs against a VSX 1021.

So a quick telnet session later I had yanked the volume up without ever leaving the kitchen!
These commands probably work for most of the VSX  921/1021 series and later. Enjoy:

Volume:
VD = VOLUME DOWN
MZ = MUTE ON/OFF
VU = VOLUME UP
?V = QUERY VOLUME

Power control:
PF = POWER OFF
PO = POWER ON
?P = QUERY POWER STATUS

Input selection:
05FN = TV/SAT
01FN = CD
03FN = CD-R/TAPE
04FN = DVD
19FN = HDMI1
05FN = TV/SAT
00FN = PHONO
03FN = CD-R/TAPE
26FN = HOME MEDIA GALLERY(Internet Radio)
15FN = DVR/BDR
05FN = TV/SAT
10FN = VIDEO 1(VIDEO)
14FN = VIDEO 2
19FN = HDMI1
20FN = HDMI2
21FN = HDMI3
22FN = HDMI4
23FN = HDMI5
24FN = HDMI6
25FN = BD
17FN = iPod/USB
FU = INPUT CHANGE (cyclic)
?F = QUERY INPUT

If you want to change input to the iPod port and turn up the volume, given you’re using OS X or some Unix derivative, you would do this:

Open a terminal
Run the command telnet <ip>
Select input by typing: 17FN<enter>
Nod volume up 1 time: VU<enter>
Repeat VU until you are happy.
There is a tone of other commands you can use, I believe this manual for the VSX 1120 is very much valid for other devices in the series.

"""
from Modules.Core.Utilities.convert import long_to_str

__updated__ = '2018-07-12'

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.error import ConnectionDone
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pioneer        ')
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

PORT = 8102
IP = '192.168.9.121'


class PioneerData(object):

    def __init__(self):
        self.DeviceCount = 0
        self.Devices = {}  # PioneerDeviceData()


class PioneerDeviceData(BaseUUIDObject):

    def __init__(self):
        super(PioneerDeviceData, self).__init__()
        self.Comment = None
        self.IPv4 = None
        self.Port = None
        self.RoomCoords = None
        self.RoomName = None
        self.RoomUUID = None
        self.Status = None
        self.Type = None
        self.Volume = None
        self._Factory = None


class XML(object):
    """
    """

    @staticmethod
    def _read_device(p_xml):
        l_device = PioneerDeviceData()
        XmlConfigTools().read_base_UUID_object_xml(l_device, p_xml)
        l_device.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = XmlConfigTools().write_base_UUID_object_xml('Device', p_obj)
        PutGetXML().put_text_element(l_xml, 'Comment', p_obj.Comment)
        PutGetXML().put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML().put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML().put_text_element(l_xml, 'Type', p_obj.Type)
        return l_xml

    @staticmethod
    def _read_one(p_xml):
        """ Read in one entire PioneerDeviceData
        """
        l_obj = XML._read_device(p_xml)
        l_obj.Status = 'off'
        l_obj.Type = 'Receiver'
        l_obj.Volume = 0
        return l_obj

    @staticmethod
    def _write_one(_p_pyhouse_obj, p_obj):
        """ Create the complete Device XML for one Pioneer device.
        """
        l_xml = XML._write_device(p_obj)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_all(p_pyhouse_obj):
        """ Get the entire PioneerData object from the xml.
        """
        l_dict = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        if l_xml == None:
            return l_dict, l_count
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml == None:
            return l_dict, l_count
        l_xml = l_xml.find('PioneerSection')
        if l_xml == None:
            return l_dict, l_count
        for l_dev_xml in l_xml.iterfind('Device'):
            l_dict[l_count] = XML._read_one(l_dev_xml)
            LOG.info('Loaded Pioneer device {}'.format(l_dict[l_count].Name))
            l_count += 1
        LOG.info('Loaded {} Pioneer Devices.'.format(l_count))
        return l_dict, l_count

    @staticmethod
    def write_all(p_pyhouse_obj):
        """ Create the entire PioneerSection of the XML.
        """
        l_xml = ET.Element('PioneerSection')
        l_count = 0
        for l_obj in p_pyhouse_obj.House.Entertainment.Pioneer.values():
            l_xml.append(XML._write_one(p_pyhouse_obj, l_obj))
            l_count += 1
        LOG.info('Saved {} Pioneer device(s) XML'.format(l_count))
        return l_xml


class PioneerProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        Protocol.dataReceived(self, p_data)
        LOG.info('Data Received.\n\tData:{}'.format(p_data))

    def connectionMade(self):
        Protocol.connectionMade(self)
        LOG.info('Connection Made.')

    def connectionLost(self, reason=ConnectionDone):
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class PioneerClient(PioneerProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj, p_pioneer_obj, _p_clientID=None):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_obj = p_pioneer_obj


class PioneerFactory(ReconnectingClientFactory):
    """
    """

    def __init__(self, p_pyhouse_obj, p_pioneer_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_obj = p_pioneer_obj
        LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_obj, 'Pioneer')))

    def startedConnecting(self, p_connector):
        # ReconnectingClientFactory.startedConnecting(self, p_connector)
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        _protocol = PioneerProtocol()
        LOG.info('BuildProtocol - Addr = {}'.format(p_addr))
        l_client = PioneerClient(self.m_pyhouse_obj, self.m_pioneer_obj)
        # l_ret = ReconnectingClientFactory.buildProtocol(self, p_addr)
        return l_client

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ This is required. """
        LOG.error('ConnectionLost.\n\tReason: {}'.format(p_reason))

    def makeConnection(self, p_transport):
        """ This is required. """
        LOG.warn('makeConnection - Transport: {}'.format(p_transport))


class Util(object):
    """
    """

    def start_factory(self):
        pass


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized")

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Pioneer devices.
        """
        p_pyhouse_obj.House.Entertainment.Pioneer = PioneerData()  # Clear before loading
        l_pioneer_obj, l_count = XML().read_all(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Pioneer = l_pioneer_obj
        LOG.info("Loaded {} XML".format(l_count))
        return l_pioneer_obj

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        l_count = 0
        for l_pioneer_obj in self.m_pyhouse_obj.House.Entertainment.Pioneer.values():
            l_count += 1
            LOG.debug('Working on device {}.'.format(l_pioneer_obj.Name))
            if not l_pioneer_obj.Active:
                continue
            l_host = long_to_str(l_pioneer_obj.IPv4)
            l_port = l_pioneer_obj.Port
            LOG.debug("Started Pioneer Host:{}; Port:{}.".format(l_host, l_port))
            l_factory = PioneerFactory(self.m_pyhouse_obj, l_pioneer_obj)
            l_pioneer_obj._Factory = l_factory
            LOG.debug('Factory {}'.format(PrettyFormatAny.form(l_factory, 'Factory')))

            l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_pioneer_obj._Factory)
            LOG.debug('Connector {}'.format(PrettyFormatAny.form(l_connector, 'Connector')))

            LOG.info("Started Pioneer {} {}.".format(l_host, l_port))
        LOG.info("Started {} Pioneer device(s).".format(l_count))

    def SaveXml(self, p_xml):
        l_xml = XML().write_all(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Pioneer XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
