"""
@name:      Modules/Core/Mqtt/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2020 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
"""

__updated__ = '2020-02-18'
__version_info__ = (20, 2, 18)
__version__ = '.'.join(map(str, __version_info__))

CLIENT_PREFIX = 'PyH-'
CONFIG_NAME = 'mqtt'


class MqttInformation:
    """

    ==> PyHouse.Core.Mqtt.xxx as in the def below
    """

    def __init__(self) -> None:
        self.Brokers: dict = {}  # MqttBrokerInformation()
        self.ClientID: str = CLIENT_PREFIX
        self.Prefix: str = ''
        self._Api = None
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
        self.Host = None
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

    def __init__(self) -> None:
        self.Topic: Optional[str] = None
        self.Payload: Optional[str] = None
        self.UnprocessedTopic: List[str] = []  # a list of topic parts
        self.LogMessage: Optional[str] = None

# ## END DBK
