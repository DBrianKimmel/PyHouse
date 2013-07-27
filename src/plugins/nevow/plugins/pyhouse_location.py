"""
Created on Jun 27, 2013

@author: briank

This must be installed under newow/plugins - see PyHouse/install/install_files for location

for win 7:
    cd /c/Users/briank/Documents/GitHub/PyHouse/src/plugins/nevow/plugins
    cp pyhouse_location.py ~/../../Python27/lib/site-packages/nevow/plugins/pyhouse_location.py


"""
from twisted.python import util
from nevow import athena


myPackage = athena.JSPackage({
    'MyModule': '/home/briank/PyHouse/src/web/js/rootmenu.js',
    })


import PyHouse
pyhousePackage = athena.AutoJSPackage(
    util.sibpath(PyHouse.__file__, 'js')
    )


from src.web.experimental import chatthing2
chatthingPkg = athena.AutoJSPackage(util.sibpath(chatthing2.__file__, 'js'))

# ## END DBK
