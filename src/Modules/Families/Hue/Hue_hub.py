"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_hub.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_hub.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
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

"""
from twisted.web.client import Agent

__updated__ = '2017-12-20'








#! /usr/bin/python

# This program was written by Folkert van Heusden.
# It is released under AGPL 3.0

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import configparser
import json
import os
import socket
import subprocess
import sys
from threading import Thread
import threading
import time
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol

main_config = dict()

ssdp_addr = '239.255.255.250'
ssdp_port = 1900

mac = [ '00', '17', '88', '10', '22', '01' ]
bridgeid = '%sFFFE%s' % (''.join(mac[0:3]), ''.join(mac[3:6]))

uid = '2f402f80-da50-11e1-9b23-%s' % ''.join(mac)

icon = 'hue.png'

description_xml = 'description.xml'

lights = []

username = "83b7780291a6ceffbe0bd049104df"
devicetype = "something"
portalservices = False

def gen_ts():
    return time.strftime('%Y-%m-%dT%H:%M:%S')

def put_config_json(j):
    entry = json.loads(j)

    if 'devicetype' in entry:
        global devicetype
        devicetype = entry['devicetype']

    elif 'portalservices' in entry:
        global portalservices
        portalservices = entry['portalservices']

def json_dumps(what):
    return json.dumps(what, sort_keys=True, separators=(',', ':'))

def gen_config_json(full):
    return json_dumps(gen_config(full))

def gen_sensors_json():
    return json_dumps(dict())

def set_light_state(nr, state):
    entry = json.loads(state)
    return json_dumps(json_obj)

def set_group_state(nr, state):
    # only 1 group in the current version
    for i in xrange(0, len(lights)):
        set_light_state(i, state)

def get_light_state(nr):

def gen_ind_light_json(nr):
    return

class gilj(Thread):
    def __init__(self, nr):
        self.nr = nr
        self.result = None
        Thread.__init__(self)

    def get_result(self):
        return self.result

    def run(self):
        self.result = gen_ind_light_json(self.nr)

def gen_lights(which):
    global lights
    if which == None:
        json_obj = dict()
        t = []
        n = 0
        for l in lights:
            th = gilj(n)
            n += 1
            th.start()
            t.append(th)
        for nr in xrange(0, n):
            t[nr].join()
            json_obj['%d' % (nr + 1)] = t[nr].get_result()
        return json_obj
    return gen_ind_light_json(which)

def gen_groups(which):
    #### a light group
    action = {
        'on': True,
        'bri': 254,
        'hue': 10000,
        'sat': 254,
        'effect': 'none',
        'xy': [],
        'ct': 250,
        'alert': 'select',
        'colormode': 'ct'
    }
    action['xy'].append(0.5)
    action['xy'].append(0.5)
    g_lights = []
    nOn = 0
    for i in xrange(0, len(lights)):
        g_lights.append('%d' % (i + 1))
        if lights[i]['state'] == True:
            nOn +=1
    state = {
        'all_on': nOn == len(lights),
        'any_on': nOn > 0
    }
    g = {
        'action': action,
        'lights': g_lights,
        'state': state,
        'type': 'Room',
        'class': 'Living room',
        'name': 'Group 1'
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
    for i in xrange(0, len(lights)):
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
        'config': gen_config(True),
        'sensors': {},
        'swupdate2': {},
        'schedules': {},
        'scenes': {}
    }
    return json_dumps(answer)

def gen_description_xml(addr):
    reply = [ '<root xmlns="urn:schemas-upnp-org:device-1-0">', 
        '<specVersion>',
        '<major>1</major>',
        '<minor>0</minor>',
        '</specVersion>',
        '<URLBase>http://%s/</URLBase>' % addr,
        '<device>',
        '<deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>',
        '<friendlyName>Virtual hue</friendlyName>',
        '<manufacturer>vanheusden.com</manufacturer>',
        '<manufacturerURL>http://www.vanheusden.com</manufacturerURL>',
        '<modelDescription>Virtual Philips hue bridge</modelDescription>',
        '<modelName>Virtual hue</modelName>',
        '<modelNumber>1</modelNumber>',
        '<modelURL>https://github.com/flok99/virtual-hue</modelURL>',
        '<serialNumber>%s</serialNumber>' % ''.join(mac),
        '<UDN>uuid:%s/UDN>' % uid,
        '<presentationURL>index.html</presentationURL>',
        '<iconList>',
        '<icon>',
        '<mimetype>image/png</mimetype>',
        '<height>48</height>',
        '<width>48</width>',
        '<depth>24</depth>',
        '<url>%s</url>' % icon,
        '</icon>',
        '</iconList>',
        '</device>',
        '</root>'
        ]
    return '\r\n'.join(reply)


class server(BaseHTTPRequestHandler):
    def _set_headers(self, mime_type):
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()

    def do_GET(self):
        print 'GET', self.client_address, self.path
        parts = self.path.split('/')
        if self.path == '/%s' % description_xml:
            self._set_headers("text/xml")
            print 'get %s' % description_xml
            h = self.server.server_address[0]
            if 'Host' in self.headers:
                h = self.headers['Host']
            self.wfile.write(gen_description_xml(h))
        elif self.path == '/%s' % icon:
            self._set_headers("image/png")
            print 'get %s' % parts[1]
            try:
                fh = open(icon, 'r')
                self.wfile.write(fh.read())
                fh.close()
            except Exception, e:
                print 'Cannot access %s' % icon, e
        elif self.path == '/api/' or self.path == '/api/%s' % username or self.path == '/api/%s/' % username:
            self._set_headers("application/json")
            print 'get all state'
            self.wfile.write(gen_dump_json())
        elif self.path == '/api/config' or self.path == '/api/config/':
            self._set_headers("application/json")
            print 'get basic configuration short (2)'
            self.wfile.write(gen_config_json(False))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'lights':
            self._set_headers("application/json")
            print 'enumerate list of lights'
            if len(parts) == 4 or parts[4] == '':
                print ' ...all'
                self.wfile.write(gen_light_json(None))
            else:
                print ' ...single (%s)' % parts[4]
                self.wfile.write(gen_light_json(int(parts[4]) - 1))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'groups':
            self._set_headers("application/json")
            print 'enumerate list of groups'
            if len(parts) == 4 or parts[4] == '':
                print ' ...all'
                self.wfile.write(gen_groups_json(None))
            else:
                print ' ...single (%s)' % parts[4]
                self.wfile.write(gen_groups_json(int(parts[4]) - 1))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'scenes':
            self._set_headers("application/json")
            print 'enumerate list of scenes'
            self.wfile.write(gen_scenes_json())
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'sensors':
            self._set_headers("application/json")
            print 'enumerate list of sensors'
            self.wfile.write(gen_sensors_json())
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'light':
            self._set_headers("application/json")
            print 'get individual light state'
            self.wfile.write(gen_ind_light_json(int(parts[4]) - 1))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'config':
            self._set_headers("application/json")
            if parts[2] == username:
                print 'get basic configuration full'
                self.wfile.write(gen_config_json(True))
            else:
                print 'get basic configuration short (1)'
                self.wfile.write(gen_config_json(False))
        else:
            self._set_headers("application/json")
            print '[G] unknown get request', self.path, self.headers
            self.wfile.write(unreg())
            #self.wfile.write('[{"error":{"type":1,"address":"/","description":"unauthorized user"}}]')

    def do_HEAD(self):
        self._set_headers("text/html")

    def do_POST(self):
        print 'POST', self.path
        parts = self.path.split('/')
        # simpler registration; always return the same key
        # should keep track in e.g. an sqlite3 database and then do whitelisting etc
        if len(parts) >= 2 and parts[1] == 'api':
            self._set_headers("application/json")
            data_len = int(self.headers['Content-Length'])
            print self.rfile.read(data_len)
            self.wfile.write('[{"success":{"username": "%s"}}]' % username)
        elif len(parts) >= 4 and parts[1] == 'api' and parts['3'] == 'groups':
            self._set_headers("application/json")
            self.wfile.write('[{"success":{"id": "1"}}]')
        else:
            print 'unknown post request', self.path

    def do_PUT(self):
        print 'PUT', self.path
        data_len = int(self.headers['Content-Length'])
        content = self.rfile.read(data_len)
        parts = self.path.split('/')
        if len(parts) >= 6 and parts[1] == 'api' and parts[3] == 'lights' and parts[5] == 'state':
            self._set_headers("application/json")
            print 'set individual light state'
            self.wfile.write(set_light_state(int(parts[4]) - 1, content))
        elif len(parts) >= 6 and parts[1] == 'api' and parts[3] == 'groups' and parts[5] == 'action':
            self._set_headers("application/json")
            print 'set individual group state'
            self.wfile.write(set_group_state(int(parts[4]) - 1, content))
        elif len(parts) >= 4 and parts[1] == 'api' and parts[3] == 'config':
            self._set_headers("application/json")
            print 'put config'
            put_config_json(content)
            self.wfile.write('[{"success":"Updated."}]')
        elif len(parts) >= 3 and parts[1] == 'api' and parts[2] == 'config':
            self._set_headers("application/json")
            print 'put config (2)'
            print content
        else:
            self._set_headers("text/html")
            print 'unknown put request', self.path, content

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(port=80):
    print 'Starting http listener...'
    h = ThreadedHTTPServer(('', port), server)
    h.serve_forever()

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

def gen_ssdp_content(addr, st_nt):
    reply = [
      "CACHE-CONTROL: max-age=100\r\n",
      "LOCATION: http://%s:80/%s\r\n" % (addr, description_xml),
      "SERVER: VirtualHue/0.1 UPNP/1.0 IpBridge/1.16.0\r\n",
      "hue-bridgeid: %s\r\n" % bridgeid,
      "%s: urn:schemas-upnp-org:device:Basic:1\r\n" % st_nt,
      "USN: uuid:%s\r\n" % uid,
      "\r\n" ]
    return ''.join(reply)

class SSDPDevice(DatagramProtocol):
    def __init__(self, addr):
        self.addr = addr
        self.ssdp = reactor.listenMulticast(ssdp_port, self, listenMultiple=True)
        self.ssdp.setLoopbackMode(1)
        self.ssdp.joinGroup(ssdp_addr, interface=addr)

    def datagramReceived(self, datagram, address):
        first_line = datagram.rsplit('\r\n')[0]
        parts = first_line.split(' ')
        if parts[0] == 'M-SEARCH':
            print "Received %s from %r" % (first_line, address, )
            # FIXME
            reply_header = [
              "HTTP/1.1 200 OK\r\n",
              "EXT:\r\n"
              ]
            reply = ''.join(reply_header) + gen_ssdp_content(self.addr, 'ST')
            self.ssdp.write(reply, address)

    def stop(self):
        self.ssdp.leaveGroup(ssdp_addr, interface=self.addr)
        self.ssdp.stopListening()

def __startSSDPListener(addr):
    obj = SSDPDevice(addr)
    reactor.addSystemEventTrigger('before', 'shutdown', obj.stop)

def _startSSDPListener(addr):
    reactor.callWhenRunning(__startSSDPListener, addr)
    reactor.run(installSignalHandlers=0)

def _startSSDPNotifier(addr):
    msgHeader = [
            'NOTIFY * HTTP/1.1\r\n',
            'HOST: 239.255.255.250:1900\r\n',
            "NTS: ssdp:alive\r\n"
        ]
    msg = ''.join(msgHeader) + gen_ssdp_content(addr, 'NT')
    while True:
        print "Sending M-NOTIFY..."
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        sock.sendto(msg, (ssdp_addr, ssdp_port))
        sock.close()
        del sock
        time.sleep(6)

def startSSDPListener(addr):
    print 'Starting SSDP listener...'
    t = Thread(target=_startSSDPListener, args=((addr),))
    t.daemon = True
    t.start()
    print 'Starting SSDP notifier...'
    t = Thread(target=_startSSDPNotifier, args=((addr),))
    t.daemon = True
    t.start()


class HueHub(object):

    def __init__(self):
        pass

    def Start(self):
        hue_agent = Agent()



# ## END DBK
