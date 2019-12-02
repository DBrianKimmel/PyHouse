"""
@name:      Modules/Core/Mqtt/mqtt_information.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 2, 2019
@summary:

"""


class MqttInformation:
    """

    ==> PyHouse.Core.Mqtt.xxx as in the def below
    """

    def __init__(self):
        self.Brokers = {}  # MqttBrokerInformation()
        self.ClientID = 'PyH-'
        self.Prefix = ''
        self._ProtocolApi = None


class MqttBrokerInformation:
    """ 0-N

    ==> PyHouse.Core.Mqtt.Brokers.XXX as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Keepalive = 60  # seconds
        #
        self.Access = None  # AccessInformation()
        self.Host = None  # HostInformation()
        self.Will = MqttBrokerWillInformation()  # MqttBrokerWillInformation()
        self.Version = 5  # We can handle versions 3,4,5 currently
        #
        self._ClientApi = None
        self._ProtocolApi = None
        self._isTLS = False


class MqttBrokerWillInformation:
    """
    ==> PyHouse.Core.Mqtt.Brokers.XXX as in the def below
    """

    def __init__(self):
        self.Topic = None
        self.Message = None
        self.QoS = 0
        self.Retain = False


class MqttJson:
    """ This is a couple of pieces of information that get added into every MQTT message
        sent out of this computer.
    """

    def __init__(self):
        self.Sender = ''  # The Mqtt name of the sending device.
        self.DateTime = None  # The time on the sending device


class MqttMessageInformation:
    """ An easy to pass message structure
    """

    def __init__(self):
        self.Topic = None
        self.Payload = None
        self.UnprocessedTopic = None
        self.LogMessage = None

# ## END DBK
