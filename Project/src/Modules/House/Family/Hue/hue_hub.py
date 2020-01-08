"""
@name:      Modules/House/Family/hue/hue_hub.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 19, 2017
@license:   MIT License
@summary:

/config
/lights
/groups
/schedules
/scenes
/sensors
/rules

Read the hub info and populate parts of pyhouse_obj.

Send hub commands to do things like turn on/off/dim of lights.

The Hue Hub is a network device so we need to know which PyHouse instance is going to be in control.

http://192.168.1.131/debug/clip.html

"""

__updated__ = '2020-01-06'

# Import system type stuff
from zope.interface import implementer
import datetime
import jsonpickle
from queue import Queue
import time
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol
from twisted.web.iweb import IBodyProducer

# Import PyMh files
from Modules.Core.Utilities.convert import long_to_str
from Modules.Core.Utilities.json_tools import encode_json
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Family.Hue.hue_data import HueLightData
from Modules.House.Lighting.utility import lightingUtility as lightingUtility

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_Hub        ')

SEND_TIMEOUT = 0.8
mac = [ '00', '17', '88', '10', '22', '01' ]
uid = '2f402f80-da50-11e1-9b23-%s' % ''.join(mac)
icon = 'hue.png'
description_xml = 'description.xml'
lights = []
username = "9nR8rIGRYNKBlROabMWuAlhGfAgSjBS2EWHoFYy3"
devicetype = "something"
portalservices = False


def generate_timestamp():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def put_config_json(p_json):
    l_entry = jsonpickle.encode(p_json)

    if 'devicetype' in l_entry:
        global devicetype
        devicetype = l_entry['devicetype']

    elif 'portalservices' in l_entry:
        global portalservices
        portalservices = l_entry['portalservices']


def json_dumps(what):
    return jsonpickle.decode(what, sort_keys=True, separators=(',', ':'))


def gen_config_json(full):
    pass
    # return json_dumps(gen_config(full))


def gen_sensors_json():
    return json_dumps(dict())


def set_light_state(_nr, state):
    _entry = jsonpickle.encode(state)
    # return json_dumps(json_obj)


def set_group_state(_nr, state):
    # only 1 group in the current version
    for i in range(0, len(lights)):
        set_light_state(i, state)


def get_light_state(nr):
    pass


def gen_ind_light_json(_nr):
    return


def gen_lights(which):
    global lights
    if which == None:
        json_obj = dict()
        t = []
        n = 0
        for _l in lights:
            th = 9875  # gilj(n)
            n += 1
            th.start()
            t.append(th)
        for nr in range(0, n):
            t[nr].join()
            json_obj['%d' % (nr + 1)] = t[nr].get_result()
        return json_obj
    return gen_ind_light_json(which)


def gen_groups(which):
    #### a light group
    action = {
        'on'        : True,
        'bri'       : 254,
        'hue'       : 10000,
        'sat'       : 254,
        'effect'    : 'none',
        'xy'        : [],
        'ct'        : 250,
        'alert'     : 'select',
        'colormode' : 'ct'
    }
    action['xy'].append(0.5)
    action['xy'].append(0.5)
    g_lights = []
    nOn = 0
    for i in range(0, len(lights)):
        g_lights.append('%d' % (i + 1))
        if lights[i]['state'] == True:
            nOn += 1
    state = {
        'all_on' : nOn == len(lights),
        'any_on' : nOn > 0
    }
    g = {
        'action' : action,
        'lights' : g_lights,
        'state'  : state,
        'type'   : 'Room',
        'class'  : 'Living room',
        'name'   : 'Group 1'
    }
    if which == None:
        answer = { '1': g }
        return answer
    return g


def gen_groups_json(which):
    return json_dumps(gen_groups(which))


def gen_scenes():
    scene = {
        'name': 'Kathy on 1449133269486',
        'lights': [],
        'owner': 'ffffffffe0341b1b376a2389376a2389',
        'recycle': True,
        'locked': False,
        'appdata': dict(),
        'picture': '',
        'lastupdated': '2015-12-03T08:57:13',
        'version': 1
    }
    for i in range(0, len(lights)):
        scene['lights'].append('%d' % (i + 1))
    answer = { '123123123-on-0':  scene }
    return answer


def gen_scenes_json():
    return json_dumps(gen_scenes())


def gen_light_json(which):
    return json_dumps(gen_lights(which))


def gen_dump_json():
    answer = {
        'lights': gen_lights(None),
        'groups': gen_groups(None),
        # 'config': gen_config(True),
        'sensors': {},
        'swupdate2': {},
        'schedules': {},
        'scenes': {}
    }
    return json_dumps(answer)


def gen_description_xml(addr):
    reply = [
        '<root xmlns="urn:schemas-upnp-org:device-1-0">',
        '  <specVersion>',
        '    <major>1</major>',
        '    <minor>0</minor>',
        '  </specVersion>',
        '  <URLBase>http://%s/</URLBase>' % addr,
        '  <device>',
        '    <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>',
        '    <friendlyName>Virtual hue</friendlyName>',
        '    <manufacturer>vanheusden.com</manufacturer>',
        '    <manufacturerURL>http://www.vanheusden.com</manufacturerURL>',
        '    <modelDescription>Virtual Philips hue bridge</modelDescription>',
        '    <modelName>Virtual hue</modelName>',
        '    <modelNumber>1</modelNumber>',
        '    <modelURL>https://github.com/flok99/virtual-hue</modelURL>',
        '    <serialNumber>%s</serialNumber>' % ''.join(mac),
        '    <UDN>uuid:%s/UDN>' % uid,
        '    <presentationURL>index.html</presentationURL>',
        '    <iconList>',
        '      <icon>',
        '        <mimetype>image/png</mimetype>',
        '        <height>48</height>',
        '        <width>48</width>',
        '        <depth>24</depth>',
        '        <url>%s</url>' % icon,
        '      </icon>',
        '    </iconList>',
        '  </device>',
        '</root>'
        ]
    return '\r\n'.join(reply)


def generate_light_body_json(p_light_control):
    """ Convert internal data to hue control data and format

    @param p_light_control: ==> LightData() in Housing.Lighting.lighting_lights
    @returns: json body to control lights
                {
                    "on": true,
                    "bri": 254
                }
    """
    if p_light_control.BrightnessPct == 0:
        l_body = {
            'on' : 'false'
            }
    else:
        l_bright = int(p_light_control.BrightnessPct * 254 / 100)
        l_body = {
            'on'  : 'true',
            'bri' : '{}'.format(l_bright)
             }
    return encode_json(l_body)


@implementer(IBodyProducer)
class BytesProducer(object):
    """
    Generate the messages to send in the web requests.
    """

    def __init__(self, body):
        self.m_body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.m_body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


# class server(BaseHTTPRequestHandler):
class Server:
    """
    """

    m_client_address = None
    m_path = '/'

    def _set_headers(self, mime_type):
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()

    def do_GET(self):
        LOG.debug('GET', self.m_client_address, self.m_path)
        parts = self.m_path.split('/')

        if self.m_path == '/{}'.format(description_xml):
            self._set_headers("text/xml")
            LOG.debug('get {}'.format(description_xml))
            h = self.Server.server_address[0]
            if 'Host' in self.headers:
                h = self.headers['Host']
            self.wfile.write(gen_description_xml(h))

        elif self.m_path == '/%s' % icon:
            self._set_headers("image/png")
            LOG.debug('get %s' % parts[1])
            try:
                fh = open(icon, 'r')
                self.wfile.write(fh.read())
                fh.close()
            except Exception as e:
                LOG.warning('Cannot access %s' % icon, e)

        elif self.m_path == '/api/' or self.m_path == '/api/%s' % username or self.m_path == '/api/%s/' % username:
            self._set_headers("application/json")
            LOG.debug('get all state')
            self.wfile.write(gen_dump_json())

        elif self.m_path == '/api/config' or self.m_path == '/api/config/':
            self._set_headers("application/json")
            LOG.debug('get basic configuration short (2)')
            self.wfile.write(gen_config_json(False))

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'lights':
            self._set_headers("application/json")
            LOG.debug('enumerate list of lights')
            if len(parts) == 4 or parts[4] == '':
                LOG.debug(' ...all')
                self.wfile.write(gen_light_json(None))
            else:
                LOG.debug(' ...single (%s)' % parts[4])
                self.wfile.write(gen_light_json(int(parts[4]) - 1))

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'groups':
            self._set_headers("application/json")
            LOG.debug('enumerate list of groups')
            if len(parts) == 4 or parts[4] == '':
                LOG.debug(' ...all')
                self.wfile.write(gen_groups_json(None))
            else:
                LOG.debug(' ...single (%s)' % parts[4])
                self.wfile.write(gen_groups_json(int(parts[4]) - 1))

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'scenes':
            self._set_headers("application/json")
            LOG.debug('enumerate list of scenes')
            self.wfile.write(gen_scenes_json())

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'sensors':
            self._set_headers("application/json")
            LOG.debug('enumerate list of sensors')
            self.wfile.write(gen_sensors_json())

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'light':
            self._set_headers("application/json")
            LOG.debug('get individual light state')
            self.wfile.write(gen_ind_light_json(int(parts[4]) - 1))

        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'config':
            self._set_headers("application/json")
            if parts[2] == username:
                LOG.debug('get basic configuration full')
                self.wfile.write(gen_config_json(True))
            else:
                LOG.debug('get basic configuration short (1)')
                self.wfile.write(gen_config_json(False))

        else:
            self._set_headers("application/json")
            LOG.debug('[G] unknown get request', self.m_path, self.headers)
            self.wfile.write('unreg()')
            # self.wfile.write('[{"error":{"type":1,"address":"/","description":"unauthorized user"}}]')

    def do_HEAD(self):
        LOG.debug('HEAD')
        self._set_headers("text/html")

    def do_POST(self):
        LOG.debug('POST', self.m_path)
        parts = self.m_path.split('/')
        # simpler registration; always return the same key
        # should keep track in e.g. an sqlite3 database and then do whitelisting etc
        if len(parts) >= 2 and parts[1] == 'api':
            self._set_headers("application/json")
            data_len = int(self.headers['Content-Length'])
            LOG.debug(self.rfile.read(data_len))
            self.wfile.write('[{"success":{"username": "%s"}}]' % username)
        elif len(parts) >= 4 and parts[1] == 'api' and parts['3'] == 'groups':
            self._set_headers("application/json")
            self.wfile.write('[{"success":{"id": "1"}}]')
        else:
            LOG.debug('unknown post request', self.m_path)

    def do_PUT(self):
        LOG.debug('PUT', self.m_path)
        data_len = int(self.headers['Content-Length'])
        content = self.rfile.read(data_len)
        parts = self.m_path.split('/')
        if len(parts) >= 6 and parts[1] == 'api' and parts[3] == 'lights' and parts[5] == 'state':
            self._set_headers("application/json")
            LOG.debug('set individual light state')
            self.wfile.write(set_light_state(int(parts[4]) - 1, content))
        elif len(parts) >= 6 and parts[1] == 'api' and parts[3] == 'groups' and parts[5] == 'action':
            self._set_headers("application/json")
            LOG.debug('set individual group state')
            self.wfile.write(set_group_state(int(parts[4]) - 1, content))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'config':
            self._set_headers("application/json")
            LOG.debug('put config')
            put_config_json(content)
            self.wfile.write('[{"success":"Updated."}]')
        elif len(parts) >= 3 and parts[1] == 'api' and parts[2] == 'config':
            self._set_headers("application/json")
            LOG.debug('put config (2)')
            LOG.debug(content)
        else:
            self._set_headers("text/html")
            LOG.debug('unknown put request', self.m_path, content)


def add_light(name, id_, command, command_get):
        global lights
        row = {
            'name': name,
            'id': id_,
            'cmd': command,
            'cmd_get': command_get,
            'state': False
        }
        lights.append(row)


class HueProtocol(Protocol):
    """ A minimal protocol for the Hue Hub.
    """

    m_finished = None
    m_remaining = 0

    def __init__(self, p_pyhouse_obj, p_finished, p_command, p_response_code):
        """
        @param p_finished: is a deferred that ????
        """
        self.m_finished = p_finished
        self.m_command = p_command
        self.m_code = p_response_code
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_body = ''
        self.m_remaining = 1024 * 10  # Allow for 10kb response
        LOG.debug('Hue Protocol Init')

    def dataReceived(self, p_bytes):
        if self.m_remaining > 0:
            l_display = p_bytes[:self.m_remaining].decode("utf8")  # Get the string
            # l_json = jsonpickle.decode(l_display)
            # LOG.debug('\n\tCommand: {}\n===== Body =====\n{}\n'.format(self.m_command, l_json))
            self.m_body = l_display
            self.m_remaining -= len(l_display)

    def connectionLost(self, p_reason):
        """ This gets called when the web page has all been received in its entirety.
        GET
            Now we have the page (and the command we used to get the page) we can deal with the servers reply.
        POST
            ?
        """

        def cb_log(self, p_command, p_code, p_body, p_finished, p_pyhouse_obj):
            """ Log the response to our command and dispatch the message
            """
            # LOG.debug('\n\tCommand: {}\n\tCode: {}\n\tBody: {}'.format(p_command, p_code, p_body))
            if p_command == '/config':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_config(p_body)
            elif p_command == '/lights':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_lights(p_body)
            elif p_command == '/rules':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_rules(p_body)
            elif p_command == '/scenes':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_scenes(p_body)
            elif p_command == '/schedules':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_schedules(p_body)
            elif p_command == '/sensors':
                HueDispatch(p_pyhouse_obj, p_finished, p_command, p_code).get_sensors(p_body)

        def eb_failed(fail_reason):
            LOG.warning("initial Hue Hub connection failed: {}".format(fail_reason))
            # l_ReconnectingService.stopService()

        l_msg = p_reason.getErrorMessage()  # this gives a tuple of messages (I think)
        if l_msg == '':
            self.m_finished.addCallback(cb_log, self.m_command, self.m_code, self.m_body, self.m_finished, self.m_pyhouse_obj)
            self.m_finished.addErrback(eb_failed, p_reason)
            self.m_finished.callback(None)
            return
        LOG.debug('Finished receiving body: {}'.format(PrettyFormatAny.form(l_msg, 'Reason', 190)))
        LOG.debug('Finished receiving body: {}'.format("\t".join(str(x) for x in l_msg)))
        self.m_finished.callback(None)
        return


class HueDecode(object):
    """
    """

    def decode_get(self):
        """
        """
        LOG.info('Decode_Get')

    def decode_post(self):
        """
        """
        LOG.info('Decode_Post')


class HueDispatch(HueProtocol):
    """
    """

    def _add_light(self, p_light_obj):
        l_objs = self.m_pyhouse_obj.House.Lighting.Lights
        _l_light_obj = lightingUtility().get_object_type_by_id(l_objs, name=p_light_obj.Name)
        pass

    def get_config(self, p_body):
        # l_msg = jsonpickle.decode(p_body)
        # LOG.debug('Got Config {}'.format(PrettyFormatAny.form(l_msg, 'Config', 190)))
        pass

    def get_lights(self, p_body):
        """
        See Docs/Design.md for the JSON returned.
        """
        LOG.debug('{}'.format(p_body))
        return

        try:
            # l_json = jsonpickle.decode(p_body)
            l_json = p_body
        except Exception as e_err:
            LOG.error('Error - {}\n{}'.format(e_err, PrettyFormatAny.form(l_json, "HUE ERROR", 190)))
        # LOG.debug('Got Lights {}'.format(PrettyFormatAny.form(l_json, 'Lights', 190)))
        for l_light_obj in l_json.items():
            l_light = HueLightData()
            LOG.debug('Light: {}'.format(PrettyFormatAny.form(l_light_obj, 'Light', 190)))
            for l_key, l_value in l_light_obj[1].items():
                l_light.HueLightIndex = l_light_obj[0]
                l_light.Key = l_light_obj[0]
                # l_light.Active = True
                l_light.Family.Name = 'Hue'
                l_light.DeviceType = 'Lighting'  # Lighting
                l_light.DeviceSubType = 'Light'
                l_light.ControllerName = 'Hue Hub'
                l_light.LastUpdate = datetime.datetime.now()
                l_light.IsDimmable = True
                # LOG.debug('Add Light: {} {}'.format(l_key, PrettyFormatAny.form(l_value, 'Light', 190)))
                if l_key == 'name':
                    l_light.Name = l_value
                    # LOG.debug('Add Light {}'.format(PrettyFormatAny.form(l_light, 'Light', 190)))
                if l_key == 'type':
                    l_light.Comment = l_value
                if l_key == 'uniqueid':
                    l_light.HueUniqueId = l_value
                if l_key == 'state':
                    l_state = False
                    for l_st_key, l_st_val in l_value.items():
                        if l_st_key == 'on':
                            l_state = l_st_val
                        if l_st_key == 'bri':
                            l_bri = l_st_val
                    if l_state == True:
                        l_light.BrightnessPct = int(l_bri / 2.54)
                    else:
                        l_light.BrightnessPct = 0
            LOG.debug('Add Light {}'.format(PrettyFormatAny.form(l_light, 'Light', 190)))
            self._add_light(l_light)

    def get_rules(self, p_body):
        l_msg = jsonpickle.decode(p_body)
        LOG.debug('Got Rules {}'.format(PrettyFormatAny.form(l_msg, 'Rules', 190)))

    def get_scenes(self, p_body):
        l_msg = jsonpickle.decode(p_body)
        LOG.debug('Got Scenes {}'.format(PrettyFormatAny.form(l_msg, 'Scenes', 190)))

    def get_schedules(self, p_body):
        l_msg = jsonpickle.decode(p_body)
        LOG.debug('Got Schedules {}'.format(PrettyFormatAny.form(l_msg, 'Schedules', 190)))

    def get_sensors(self, p_body):
        l_msg = jsonpickle.decode(p_body)
        LOG.debug('Got Sensors {}'.format(PrettyFormatAny.form(l_msg, 'Sensors', 190)))


class HueHub:
    """
    """

    m_bridge_obj = None
    m_command = b'/config'
    m_headers = None
    m_hue_agent = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        Agent is a very basic HTTP client.  It supports I{HTTP} and I{HTTPS} scheme URIs.

        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_headers = Headers({'User-Agent': ['Hue Hub Web Client']})
        self.m_hue_agent = Agent(p_pyhouse_obj._Twisted.Reactor)
        LOG.info('Initialized')

    def _build_uri(self, p_command=b'/config'):
        """
        URI: b'http://192.168.1.131/api/MBFBC-agf6rq5bsWcxLngYZoClGr2pw2oKEMLZgs/config'
        """
        l_uri = b'http://'
        try:
            l_uri += self.m_bridge_obj.IPv4Address
        except TypeError:
            l_uri += long_to_str(self.m_bridge_obj.IPv4Address).encode("utf8")
        l_uri += b'/api/'
        try:
            l_uri += self.m_bridge_obj.ApiKey
        except TypeError:
            l_uri += self.m_bridge_obj.ApiKey.encode("utf8")
        try:
            l_uri += p_command.encode("utf8")
        except:
            l_uri += p_command
        LOG.info('URI: {}'.format(l_uri))
        return l_uri

    def _build_command(self, p_command):
        try:
            l_command = p_command.encode("utf8")
        except:
            l_command = p_command
        return l_command

    def _get_all_config(self):
        """
        /config
        /lights
        /groups
        /schedules
        /scenes
        /sensors
        /rules
        """
        return

        _l_agent_d = self.HubGet('/config')
        _l_agent_d = self.HubGet('/lights')
        # _l_agent_d = self.HubGet('/groups')
        # _l_agent_d = self.HubGet('/schedules')
        # _l_agent_d = self.HubGet('/scenes')
        # _l_agent_d = self.HubGet('/sensors')
        # _l_agent_d = self.HubGet('/rules')
        # Server().do_GET()
        LOG.info('Scheduled All config')

    def HubGet(self, p_command):
        """ Issue a request for information.  It will arrive later via a deferred.
        """

        def cb_Response(p_response, p_command):
            """
            """
            # LOG.debug('Command: {}'.format(p_command))
            # LOG.debug('Response Code: {} {}'.format(p_response.code, p_response.phrase))
            d_finished = Deferred()
            p_response.deliverBody(HueProtocol(self.m_pyhouse_obj, d_finished, p_command, p_response.code))
            return d_finished

        d_agent = self.m_hue_agent.request(
            b'GET',
            self._build_uri(p_command),
            self.m_headers,
            None)
        d_agent.addCallback(cb_Response, p_command)
        HueDecode().decode_get()
        return d_agent

    def HubPostCommand(self, p_command, p_body):
        """
        @param p_command: is the Hue command we will be using
        @param p_body: is the body producer function.
        """

        def cb_response(p_response):
            LOG.debug('Response Code: {} {}'.format(p_response.code, p_response.phrase))
            LOG.debug('Response Headers: {}'.format(p_response.headers.decode("utf8")))
            l_finished = Deferred()
            p_response.deliverBody(HueProtocol(self.m_pyhouse_obj, l_finished))
            return l_finished

        l_agent_d = self.m_hue_agent.request(b'POST',
                                             self._build_uri(p_command),
                                             self.m_headers,
                                             p_body)
        l_agent_d.addCallback(cb_response)
        HueDecode().decode_post()
        return l_agent_d

    def HubStart(self, p_bridge_obj):
        """ Start the hub(bridge) and then get the hub data

        @param p_bridge_obj: is PyHouse_Obj.Computers.Bridges.xxx with xxx being a HueHub

        """
        p_bridge_obj._Queue = Queue(32)
        self.m_bridge_obj = p_bridge_obj
        self._get_all_config()
        LOG.info('Started')

    def Start(self):
        """ Start the hub(bridge) and then get the hub data

        @param p_bridge_obj: is PyHouse_Obj.Computers.Bridges.xxx with xxx being a HueHub

        """
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'Computer'))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'House'))
        for l_bridge_obj in self.m_pyhouse_obj.Computer.Bridges.values():
            LOG.debug(PrettyFormatAny.form(l_bridge_obj, 'Bridge'))
            l_bridge_obj._Queue = Queue(32)
            self.m_bridge_obj = l_bridge_obj
            self._get_all_config()
        LOG.debug('Started')

# ## END DBK
