"""
@name:      C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/Nodes/node_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:


topic scheme:
    PyHouse/<Domain UUID>/<HouseIdentifier>/<Device Specific>
    Where <Device Specific> is:
        <Location>/<Function>/<Action>
            <Location> = Room Name or some other description
            <Function> = Temperature, LightLevel, HumanDetected, Rainfall, WindSpeed etc.
            <Action> = Reading, TurnOn, TurnOff to list a few.
    There are no spaces in any of the sections.


<mqtt>
    <BrokerIp4 />
    <BrokerIp6 />
</mqtt>

"""

# Import system type stuff
from paho.mqtt import client as mqtt

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Nodes import nodes_xml

LOG = Logger.getLogger('PyHouse.NodeMqtt       ')


class Util(object):

    @staticmethod
    def on_connect():
        pass

    @staticmethod
    def on_data_received():
        pass


class API(object):

    m_pyhouse_obj = None
    m_client = None

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # Read xml data
        self.m_client = mqtt.Client()
        self.m_client.on_connect = Util.on_connect
        self.m_client.on_message = Util.on_message
        self.m_client.connect("iot.eclipse.org", 1883, 60)



    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        p_xml.append(nodes_xml.Xml().write_nodes_xml(self.m_pyhouse_obj.Computer.Nodes))
        LOG.info("Saved XML.")



# ## END DBK
