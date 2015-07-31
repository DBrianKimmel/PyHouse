"""
@name:      PyHouse/src/Modules/Computer/test/xml_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 8, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Communication.test.xml_communications import XML_COMMUNICATION
from Modules.Computer.Internet.test.xml_internet import XML_INTERNET
from Modules.Computer.Mqtt.test.xml_mqtt import XML_MQTT
from Modules.Computer.Nodes.test.xml_nodes import XML_NODES
from Modules.Web.test.xml_web import XML_WEB_SERVER


COMPUTER_DIVISION_XML = '\n'.join([
    "<ComputerDivision>",
    XML_NODES,
    XML_COMMUNICATION,
    XML_WEB_SERVER,
    XML_INTERNET,
    XML_MQTT,
    "</ComputerDivision>",
    ''
])


COMPUTER_XSD = """
"""

# ## END DBK