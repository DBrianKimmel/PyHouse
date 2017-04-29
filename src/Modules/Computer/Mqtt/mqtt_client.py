"""
-*- test-case-name: PyHouse.Modules.Computer.Mqtt.test.test_computer -*-

@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:   Connect this computer node to the household Mqtt Broker.

"""

__updated__ = '2017-04-26'

#  Import system type stuff
from twisted.internet import defer
# from twisted.internet.endpoints import SSL4ClientEndpoint
# from twisted.internet.ssl import Certificate, optionsForClientTLS

#  Import PyMh files and modules.
from Modules.Computer.Mqtt.mqtt_protocol import PyHouseMqttFactory
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt_Client    ')

PEM_FILE = '/etc/pyhouse/ca_certs/rootCA.pem'


class Struct:
    def __init__(self, **args):
        self.__dict__.update(args)


class Util(object):
    """
    """

    def _make_client_name(self, p_pyhouse_obj):
        l_client_name = 'PyH-Computer-' + p_pyhouse_obj.Computer.Name
        return l_client_name

    def connect_to_one_broker_TCP(self, p_pyhouse_obj, p_broker):
        l_clientID = self._make_client_name(p_pyhouse_obj)
        l_host = p_broker.BrokerAddress
        l_port = p_broker.BrokerPort
        l_username = p_broker.UserName
        l_password = p_broker.Password
        l_keepalive = 60
        # p_broker._ClientAPI = self
        LOG.info('Connecting via TCP...')

        if l_host is None or l_port is None:
            LOG.error('Bad Mqtt broker Address: {}  or Port: {}'.format(l_host, l_port))
            p_broker._ProtocolAPI = None
        else:
            l_factory = PyHouseMqttFactory(p_pyhouse_obj, l_clientID, p_broker, l_username, l_password)
            _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
            LOG.info('TCP Connected to broker: {}; Host: {};'.format(p_broker.Name, l_host))
            LOG.info('Prefix: {}'.format(p_pyhouse_obj.Computer.Mqtt.Prefix))

    @defer.inlineCallbacks
    def connect_to_one_broker_TLS(self, p_pyhouse_obj, p_broker):
        l_clientID = self._make_client_name(p_pyhouse_obj)
        l_host = p_broker.BrokerAddress
        l_port = p_broker.BrokerPort
        l_username = p_broker.UserName
        l_password = p_broker.Password
        l_keepalive = p_broker.Keepalive
        # p_broker._ClientAPI = self
        LOG.info('Connecting via TLS...')
        # l_factory = protocol.Factory.forProtocol(echoclient.EchoClient)
        # l_factory = PyHouseMqttFactory(p_pyhouse_obj, l_clientID, p_broker, l_username, l_password)
        # l_certData = PEM_FILE.getContent()
        # l_authority = Certificate.loadPEM(l_certData)
        # l_options = optionsForClientTLS(l_host.decode('utf-8'), l_authority)
        # l_endpoint = SSL4ClientEndpoint(p_pyhouse_obj.Twisted.Reactor, l_host, l_port, l_options)
        # l_client = yield l_endpoint.connect(l_factory)
        l_done = defer.Deferred()
        # l_client.connectionLost = lambda reason: l_done.callback(None)
        yield l_done

    def connect_to_all_brokers(self, p_pyhouse_obj):
        """
        This will create a connection for each active broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        l_count = 0
        for l_broker in p_pyhouse_obj.Computer.Mqtt.Brokers.values():
            if not l_broker.Active:
                LOG.info('Skipping not active broker: {}'.format(l_broker.Name))
                continue
            if l_broker.BrokerPort < 2000:
                self.connect_to_one_broker_TCP(p_pyhouse_obj, l_broker)
            else:
                self.connect_to_one_broker_TLS(p_pyhouse_obj, l_broker)
            l_count += 1
        LOG.info('TCP Connected to {} Broker(s).'.format(l_count))
        return l_count

# ## END DBK
