"""
@name:      PyHouse/src/Modules/Computer/Mqtt/_test/xml_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

<?xml version="1.0" ?>
<MqttSection>
    <Broker Active="True" Key="0" Name="CannonTrail">
        <UUID>Broker..-0000-0000-0000-0123456789ab</UUID>
        <BrokerAddress>192.168.9.10</BrokerAddress>
        <BrokerPort>8883</BrokerPort>
        <BrokerUser>pyhouse</BrokerUser>
        <BrokerPassword>ChangeMe</BrokerPassword>
        <Class>Local</Class>
    </Broker>
    <Broker Active="True" Key="1" Name="PinkPoppy">
        <UUID>Broker..-0001-0001-0001-0123456789ab</UUID>
        <BrokerAddress>192.168.1.10</BrokerAddress>
        <BrokerPort>1883</BrokerPort>
        <BrokerUser>pyhouse</BrokerUser>
        <BrokerPassword>ChangeMe</BrokerPassword>
        <Class>Local</Class>
    </Broker>
</MqttSection>

"""

__updated__ = '2019-05-23'

#  Import system type stuff

#  Import PyMh files

TESTING_MQTT_SECTION = 'MqttSection'
TESTING_MQTT_BROKER = 'Broker'

L_MQTT_SECTION_START = '<' + TESTING_MQTT_SECTION + '>'
L_MQTT_SECTION_END = '  </' + TESTING_MQTT_SECTION + '>'
L_MQTT_BROKER_END = '    </' + TESTING_MQTT_BROKER + '>'

TESTING_MQTT_CLIENT_ID = 'PyH-Comp-pi-99-ct'

TESTING_BROKER_NAME_0 = 'CannonTrail'
TESTING_BROKER_KEY_0 = '0'
TESTING_BROKER_ACTIVE_0 = 'True'
TESTING_BROKER_UUID_0 = 'Broker..-0000-0000-0000-0123456789ab'
TESTING_BROKER_HOST_0 = 'mqtt-pp'
TESTING_BROKER_ADDRESS_0 = '192.168.9.10'
TESTING_BROKER_PORT_0 = '8883'
TESTING_BROKER_USERNAME_0 = 'pyhouse'
TESTING_BROKER_PASSWORD_0 = 'ChangeMe'
TESTING_BROKER_CLASS_0 = 'Local'

L_BROKER_START_0 = '    ' + \
    '<' + TESTING_MQTT_BROKER + ' ' + \
    'Name="' + TESTING_BROKER_NAME_0 + '" ' + \
    'Key="' + TESTING_BROKER_KEY_0 + '" ' + \
    'Active="' + TESTING_BROKER_ACTIVE_0 + '"' + \
    '>'
L_BROKER_UUID_0 = '      <UUID>' + TESTING_BROKER_UUID_0 + '</UUID>'
L_BROKER_ADDRESS_0 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_0 + '</BrokerAddress>'
L_BROKER_HOST_0 = '      <BrokerHost>' + TESTING_BROKER_HOST_0 + '</BrokerHost>'
L_BROKER_PORT_0 = '      <BrokerPort>' + TESTING_BROKER_PORT_0 + '</BrokerPort>'
L_BROKER_USER_0 = '      <BrokerUser>' + TESTING_BROKER_USERNAME_0 + '</BrokerUser>'
L_BROKER_PASSWORD_0 = '      <BrokerPassword>' + TESTING_BROKER_PASSWORD_0 + '</BrokerPassword>'
L_BROKER_CLASS_0 = '      <Class>' + TESTING_BROKER_CLASS_0 + '</Class>'

L_BROKER_0 = '\n'.join([
    L_BROKER_START_0,
    L_BROKER_UUID_0,
    L_BROKER_ADDRESS_0,
    L_BROKER_HOST_0,
    L_BROKER_PORT_0,
    L_BROKER_USER_0,
    L_BROKER_PASSWORD_0,
    L_BROKER_CLASS_0,
    L_MQTT_BROKER_END
])

TESTING_BROKER_NAME_1 = 'PinkPoppy'
TESTING_BROKER_KEY_1 = '1'
TESTING_BROKER_ACTIVE_1 = 'True'
TESTING_BROKER_UUID_1 = 'Broker..-0001-0001-0001-0123456789ab'
TESTING_BROKER_ADDRESS_1 = '192.168.1.10'
TESTING_BROKER_HOST_1 = 'Mqtt-ct'
TESTING_BROKER_PORT_1 = '1883'
TESTING_BROKER_USERNAME_1 = 'pyhouse'
TESTING_BROKER_PASSWORD_1 = 'ChangeMe'
TESTING_BROKER_CLASS_1 = 'Local'

L_BROKER_START_1 = '    ' + \
    '<' + TESTING_MQTT_BROKER + ' ' + \
    'Name="' + TESTING_BROKER_NAME_1 + '" ' + \
    'Key="' + TESTING_BROKER_KEY_1 + '" ' + \
    'Active="' + TESTING_BROKER_ACTIVE_1 + '"' + \
    '>'
L_BROKER_UUID_1 = '      <UUID>' + TESTING_BROKER_UUID_1 + '</UUID>'
L_BROKER_ADDRESS_1 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_1 + '</BrokerAddress>'
L_BROKER_HOST_1 = '      <BrokerHost>' + TESTING_BROKER_HOST_1 + '</BrokerHost>'
L_BROKER_PORT_1 = '      <BrokerPort>' + TESTING_BROKER_PORT_1 + '</BrokerPort>'
L_BROKER_USER_1 = '      <BrokerUser>' + TESTING_BROKER_USERNAME_1 + '</BrokerUser>'
L_BROKER_PASSWORD_1 = '      <BrokerPassword>' + TESTING_BROKER_PASSWORD_1 + '</BrokerPassword>'
L_BROKER_CLASS_1 = '      <Class>' + TESTING_BROKER_CLASS_1 + '</Class>'

L_BROKER_1 = '\n'.join([
    L_BROKER_START_1,
    L_BROKER_UUID_1,
    L_BROKER_ADDRESS_1,
    L_BROKER_HOST_1,
    L_BROKER_PORT_1,
    L_BROKER_USER_1,
    L_BROKER_PASSWORD_1,
    L_BROKER_CLASS_1,
    L_MQTT_BROKER_END
])

XML_MQTT = '\n'.join([
    L_MQTT_SECTION_START,
    L_BROKER_0,
    L_BROKER_1,
    L_MQTT_SECTION_END
    ])

#  ## END DBK
