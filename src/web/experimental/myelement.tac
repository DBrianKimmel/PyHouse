# myelement.tac

from nevow import athena, loaders, tags as T
from nevow import appserver
from twisted.application import service, internet

class MyElement(athena.LiveElement):
    docFactory = loaders.stan(
    	T.div(render=T.directive('liveElement'))[
    		'DBK-01',
        	T.input(type='submit', value='Push me',
            		onclick='Nevow.Athena.Widget.get(this).clicked()'
            )  # input
		]  # div
	)  # stan


class WhateverElement(athena.LiveElement):

  @athena.expose
  def getNewLiveElement(self):
    return SomeOtherLiveElement()




class MyPage(athena.LivePage):
    docFactory = loaders.xmlfile('/home/briank/workspace/PyHouse/src/web/experimental/page_01.xml')
#    docFactory = loaders.stan(
#    	T.html[
#    		T.head(render = T.directive('liveglue')),
#    		T.body(render = T.directive('myElement'))
#    	]  # html
#    )  # stan

    def render_myElement(self, ctx, data):
        f = MyElement()
        f.setFragmentParent(self)
        return ctx.tag[f]

    def child_(self, ctx):
        return MyPage()

site = appserver.NevowSite(MyPage())

application = service.Application('Athena Demo')
webService = internet.TCPServer(8080, site)
webService.setServiceParent(application)


# END







