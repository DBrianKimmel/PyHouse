#!/usr/bin/python

"""Entertainment component access module.
This is a Main Module - always present.

Can act as a UPnP Control point

"""

# Import system type stuff
import logging
#from twisted.web import xmlrpc, client
from twisted.internet import reactor

# Import PyMh files
from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
from coherence.upnp.core import DIDLLite
from coherence.upnp.core import ssdp
from coherence.upnp.core.msearch import MSearch
from coherence.upnp.devices.dimmable_light import DimmableLight
from coherence.upnp.devices.dimmable_light_client import DimmableLightClient
from coherence.upnp.services.servers.dimming_server import DimmingServer

Entertainment_Data = {}
g_debug = 10
g_logger = None
g_upnp = None

callLater = reactor.callLater
callWhenRunning = reactor.callWhenRunning




class EntertainmentAPI(object):
    """
    """

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class UPnPControlPoint(object):
    """
    0.  Addressing - not needed since we already have an IP address.
    1.  Discovery - Using SSDP to advertise and discover other UPnP thingies.
    2.  Description - XML queries back and forth to provide details of UPnP workings.
    3.  Control - A UPnP control point controls UPnP devices.
    4.  Eventing - How a device gets notified about happenings in the UPnP network.
    5.  Presentation - How to retrieve content from a UPnP device.
    """

    def __init__(self):
        if g_debug > 0: print "entertainment.UPnPControlPoint.__init__()"
        callWhenRunning(self.start)
        callLater(60, self.lights_on)
        callLater(120, self.lights_off)
        self.devices = []

    def discover(self):
        """Discover devices.

        Through discovery, control points find interesting device(s).
        Discovery enables description (Step 2) where control points learn about device capabilities,
        control (Step 3) where a control point sends commands to device(s),
        eventing (Step 4) where control points listen to state changes in device(s),
        and presentation (Step 5) where control points display a user interface for device(s).
        """
        #MSearch().double_discover()
        pass

    def description(self):
        """
        Where control points learn about device capabilities.
        """
        pass

    def control(self):
        """
        Where a control point sends commands to device(s).
        """
        pass

    def eventing(self):
        """
        Where control points listen to state changes in device(s).
        """
        pass

    def presentation(self):
        """
        Where control points display a user interface for device(s).
        """
        pass

    def check_device(self, device):
        """
        @param device: an instance of coherence.upnp.core.Device()
        """
        print "__Found device:{0:s}, Type:{1:s}, Client:{2:}, Id:{3:}".format(device.get_friendly_name(), device.get_device_type(), device.client, device.get_id())
        if not device in self.devices:
            self.devices.append(device)

    def state_variable_change(self, p_variable):
        if p_variable.name == 'CurrentTrackMetaData':
            if p_variable.value != None and len(p_variable.value) > 0:
                try:
                    elt = DIDLLite.DIDLElement.fromString(p_variable.value)
                    for item in elt.getItems():
                        print "__Variable - CurrentTrackMetaData - Now playing: %r - %r (%s/%r)" % (item.artist, item.title, item.id, item.upnp_class)
                except SyntaxError:
                    print "__Variable - CurrentTrackMetaData - Seems we haven't got an XML string"
                    return
        elif p_variable.name == 'TransportState':
            print '__Variable - TransportState - Changed from:{0:}, To:{1:}'.format(p_variable.old_value, p_variable.value)
        elif p_variable.name == 'ExternalIPAddress':
            print "__Our external IP address is %r" % p_variable.value
        elif p_variable.name == 'PortMappingNumberOfEntries':
            if p_variable.value != '':
                print "__There are %d port-mappings defined" % int(p_variable.value)
            else:
                print "__There are no port-mappings defined"
        elif p_variable.name == 'LoadLevelTarget':
            print '__Variable - LoadLevelTarget - {0:}'.format(p_variable.value)
        elif p_variable.name == 'LoadLevelStatus':
            print '__Variable - LoadLevelStatus - {0:}'.format(p_variable.value)

    def process_media_server_browse(self, result, client):
        print "__Browsing root of", client.device.get_friendly_name()
        print "__Result contains %d out of %d total matches" % (int(result['NumberReturned']), int(result['TotalMatches']))
        elt = DIDLLite.DIDLElement.fromString(result['Result'])
        for item in elt.getItems():
            if item.upnp_class.startswith("object.container"):
                print "__  container %s (%s) with %d items" % (item.title, item.id, item.childCount)
            if item.upnp_class.startswith("object.item"):
                print "__  item %s (%s)" % (item.title, item.id)

    def media_server___found(self, client, udn):
        """
        Called for each media server found.
        """
        print "__Media_server_found", client
        print "__Media_server_found",
        d = client.content_directory.browse(0, browse_flag = '++BrowseDirectChildren', process_result = False, backward_compatibility = False)
        d.addCallback(self.process_media_server_browse, client)

    def media_server_removed(self, udn):
    # sadly they sometimes get removed as well :(
        print "__Media_server_removed", udn

    def media_renderer_found(self, client, udn):
        #print "__Media_renderer_found", client
        print "__Media_renderer_found", client.device.get_friendly_name()
        client.av_transport.subscribe_for_variable('CurrentTrackMetaData', self.state_variable_change)
        client.av_transport.subscribe_for_variable('TransportState', self.state_variable_change)

    def media_render_removed(self, udn):
        print "__Media_renderer_removed", udn

    def igd_found(self, p_client, p_udn):
        print "__IGD found", p_client.device.get_friendly_name()
        wan_ip_connection_service = p_client.wan_device.wan_connection_device.wan_ip_connection
        wan_ip_connection_service.subscribe_for_variable('PortMappingNumberOfEntries', callback = self.state_variable_change)
        wan_ip_connection_service.subscribe_for_variable('ExternalIPAddress', callback = self.state_variable_change)

    def igd_removed(self, p_udn):
        print "__IGD_removed", p_udn

    def light_found(self, client, udn):
        print "__Light_found", udn, client.device.get_friendly_name()
        dim_service = client.dimming.dimmable
        dim_service.subscribe_for_variable('LoadLevelTarget', callback = self.state_variable_change)
        dim_service.subscribe_for_variable('LoadLevelStatus', callback = self.state_variable_change)


    def lights_on(self):
        print "Turning all lights on..."
        for l_device in self.devices:
            l_type = l_device.get_friendly_device_type()
            if l_type == 'BinaryLight':
                print " -- ", l_device.__dict__
                pass
            elif l_type == 'DimmableLight':
                #print " == ", l_device.__dict__
                l_light = DimmableLightClient(l_device)
                l_level = l_light.dimming.get_load_level_target()
                print " ~~ Before light {0:} is at level {1:}".format(l_device.get_friendly_name(), l_level)
                l_light.dimming.set_load_level_target(50)
                l_level = l_light.dimming.get_load_level_target()
                print " ~~ After light {0:} is at level {1:}".format(l_device.get_friendly_name(), l_level)
                pass
            print " - {0:}, {1:}".format(l_device.get_friendly_name(), l_device.get_friendly_device_type())
        pass

    def lights_off(self):
        print "Turning all lights off..."
        pass


        """
http://<VERA_IP>:3480/data_request?id=lu_action&DeviceNum=<ID>&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget=<LEVEL>
Will set a dimmable lite with device number <ID> to level <LEVEL>
        """

    def start(self):
        print "entertainment.UPnPControlPoint.start()"
        self.discover()
        control_point = ControlPoint(Coherence({'logmode':'warning',
                            'subsystem_log':{'coherence':'warning', 'simple_light':'debug', 'better_light':'debug', 'dimminglight_client':'debug'}}),
                            #auto_client = ['MediaRenderer']
                            )
        control_point.connect(self.check_device, 'Coherence.UPnP.Device.detection_completed')
        control_point.connect(self.light_found, 'Coherence.UPnP.ControlPoint.BinaryLight.detected')
        control_point.connect(self.light_found, 'Coherence.UPnP.ControlPoint.DimmableLight.detected')
        control_point.connect(self.media_server___found, 'Coherence.UPnP.ControlPoint.MediaServer.detected')
        control_point.connect(self.media_server_removed, 'Coherence.UPnP.ControlPoint.MediaServer.removed')
        control_point.connect(self.media_renderer_found, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected')
        control_point.connect(self.media_render_removed, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed')
        control_point.connect(self.igd_found, 'Coherence.UPnP.ControlPoint.InternetGatewayDevice.detected')
        control_point.connect(self.igd_removed, 'Coherence.UPnP.ControlPoint.InternetGatewayDevice.removed')


def Init():
    global g_logger, g_upnp
    if g_debug > 0: print "Entertainment.Init()"
    g_logger = logging.getLogger('PyMh.Entertainment')
    g_logger.info("Initializing.")
    g_upnp = UPnPControlPoint()
    g_logger.info("Initialized.")

def Start():
    pass

def Stop():
    pass

### END
