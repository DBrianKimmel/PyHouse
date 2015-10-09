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


TESTING_COMPUTER_NAME_0 = 'TestingComputer'
TESTING_COMPUTER_KEY_0 = '0'
TESTING_COMPUTER_ACTIVE_0 = 'True'
TESTING_COMPUTER_UUID = '12345678-9ABC-DEFF-1001-123456789ABC'

L_COMPUTER_DIV_START = '<ComputerDivision Name="' + TESTING_COMPUTER_NAME_0 + '" Key="' + TESTING_COMPUTER_KEY_0 + '" Active="' + TESTING_COMPUTER_ACTIVE_0 + '">'
L_COMPUTER_DIV_END = '</ComputerDivision>'
L_COMPUTER_UUID = '<UUID>' + TESTING_COMPUTER_UUID + '</UUID>'

XML_COMPUTER_DIVISION = '\n'.join([
    L_COMPUTER_DIV_START,
    L_COMPUTER_UUID,
    XML_NODES,
    XML_COMMUNICATION,
    XML_WEB_SERVER,
    XML_INTERNET,
    XML_MQTT,
    L_COMPUTER_DIV_END
])


XSD_COMPUTER_DIVISION = """
"""

# ## END DBK
