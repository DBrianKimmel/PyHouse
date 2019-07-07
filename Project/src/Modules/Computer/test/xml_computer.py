"""
@name:      PyHouse/src/Modules/Computer/test/xml_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 8, 2014
@Summary:


ComputerDivision - Name, Key, Active
  BridgeSection
  CommunicationSection
  InternetSection
  MqttSection
  NodeSection
  WebSection

"""

__updated__ = '2019-07-06'

# Import system type stuff

# Import PyMh files
from Modules.Computer.Bridges.test.xml_bridges import XML_BRIDGES
from Modules.Computer.Communication.test.xml_communications import XML_COMMUNICATION
from Modules.Computer.Internet.test.xml_internet import XML_INTERNET
from Modules.Core.Mqtt.test.xml_mqtt import XML_MQTT
from Modules.Computer.Nodes.test.xml_nodes import XML_NODES
from Modules.Computer.Web.test.xml_web import XML_WEB_SERVER

TESTING_COMPUTER_DIVISION = 'ComputerDivision'

L_COMPUTER_DIVISION_END = '  </' + TESTING_COMPUTER_DIVISION + '>'

TESTING_COMPUTER_NAME = 'TestingComputer'
TESTING_COMPUTER_KEY = '0'
TESTING_COMPUTER_ACTIVE = 'True'
TESTING_COMPUTER_COMMENT = 'This is the testing computer'
TESTING_COMPUTER_PRIORITY = '17'
TESTING_COMPUTER_UUID = 'Computer-0000-0000-0000-123456789ABC'

L_COMPUTER_DIV_START = \
    '<' + TESTING_COMPUTER_DIVISION + ' ' + \
    'Name="' + TESTING_COMPUTER_NAME + '" ' + \
    'Key="' + TESTING_COMPUTER_KEY + '" ' + \
    'Active="' + TESTING_COMPUTER_ACTIVE + '"' + \
    '>'
L_COMPUTER_UUID = '<UUID>' + TESTING_COMPUTER_UUID + '</UUID>'
L_COMPUTER_COMMENT = '<Comment>' + TESTING_COMPUTER_COMMENT + '</Comment>'
L_COMPUTER_PRIORITY = '<Priority>' + TESTING_COMPUTER_PRIORITY + '</Priority>'

XML_COMPUTER_DIVISION = '\n'.join([
    L_COMPUTER_DIV_START,
    L_COMPUTER_UUID,
    L_COMPUTER_COMMENT,
    L_COMPUTER_PRIORITY,
    XML_BRIDGES,
    XML_COMMUNICATION,
    XML_INTERNET,
    XML_MQTT,
    XML_NODES,
    XML_WEB_SERVER,
    L_COMPUTER_DIVISION_END
])

# ## END DBK
