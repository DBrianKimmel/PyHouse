"""
@name:      PyHouse/src/Modules/Computer/Mqtt/broker.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

"""

# Import system type stuff
import copy

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt import mqtt_xml, protocol
from Modules.Web import web_utils


LOG = Logger.getLogger('PyHouse.MqttBroker     ')

BROKERv4 = '192.168.1.71'
BROKERv4 = 'iot.eclipse.org'  # Sandbox Mosquitto broker
# BROKERv6 = '2604:8800:100:8268::1:1'    # Pink Poppy
BROKERv6 = '2001:4830:1600:84ae::1'  # Cannon Trail
PORT = 1883
SUBSCRIBE = 'pyhouse/#'


class Util(object):
    """
    The observations client allows a user to obtain BoM observations for a specified URL.
    """

    def __init__(self):
        self.m_connection = None

    def mqtt_start(self, p_pyhouse_obj):
        """ Start the async connection process.

        This is the twisted part.
        The connection of the MQTT protocol is kicked off after the TCP connection is complete.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        print("Broker mqtt_start")
        p_pyhouse_obj.Twisted.Reactor.connectTCP(BROKERv4, PORT, protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))


class API(Util):
    """This interfaces to all of PyHouse.
    """

    m_pyhouse_obj = None
    m_client = None

    def Start(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.MqttAPI = self
        self.m_pyhouse_obj = p_pyhouse_obj
        mqtt_xml.ReadWriteConfigXml().read_mqtt_xml(p_pyhouse_obj)
        self.m_mqtt = self.mqtt_start(p_pyhouse_obj)
        LOG.info("Broker Started.")

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        # p_xml.append(nodes_xml.Xml().write_nodes_xml(self.m_pyhouse_obj.Computer.Nodes))
        LOG.info("Saved XML.")

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list
        """
        print("Broker MqttPublish {} {}".format(p_topic, p_message))
        Util().doPublishMessage(self.m_client, p_topic, p_message)

    def MqttDispatch(self, _p_topic, _p_message):
        """Dispatch a MQTT message according to the topic.
        """
        print("MqttDispatch")
        pass

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """Login to PyHouse via MQTT
        """
        l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[0])
        l_node.NodeInterfaces = None
        l_json = web_utils.JsonUnicode().encode_json(l_node)
        print("Broker - send initial login.")
        p_client.publish('pyhouse/login/initial', l_json)

# ## END DBK
