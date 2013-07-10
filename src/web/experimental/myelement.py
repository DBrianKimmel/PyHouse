"""

myelement.py

Created on Jun 28, 2013

@author: briank

cd ~/workspace/PyHouse
twistd -noy src/web/experimental/myelement.tac

"""

from nevow import athena, loaders, tags as T
from nevow import appserver
from twisted.application import service, internet


class MyElement(athena.LiveElement):
    docFactory = loaders.stan(
        T.div(render = T.directive('liveElement'))[
            'DBK_01',
            T.input(type = 'submit', value = 'Push me',
                        onclick = 'Nevow.Athena.Widget.get(this).clicked()'
            )  # input
        ]  # div
    )  # stan


class SomeOtherLiveElement(object):
    pass


class WhateverElement(athena.LiveElement):

    @athena.expose
    def getNewLiveElement(self):
        return SomeOtherLiveElement()


class MyPage(athena.LivePage):
    docFactory = loaders.xmlfile('/home/briank/workspace/PyHouse/src/web/experimental/page_01.xml')
    # docFactory = loaders.stan(T.html[T.head(render = T.directive('liveglue')),T.body(render = T.directive('myElement'))])

    def render_myElement(self, ctx, _data):
        f = MyElement()
        f.setFragmentParent(self)
        return ctx.tag[f]

    def child_(self, _ctx):
        return MyPage()

l_site = appserver.NevowSite(MyPage())
l_application = service.Application('Athena Demo')
l_webService = internet.TCPServer(8080, l_site)
l_webService.setServiceParent(l_application)

# END
