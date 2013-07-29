"""
Created on Jun 27, 2013

@author: briank

This must be installed under newow/plugins - see PyHouse/install/install_files for location

for Linux:
    cp ~/workspace/PyHouse/src/plugins/nevow/plugins/pyhouse_location.py   /usr/local/lib/python2.7/site-packages/nevow/plugins/pyhouse_location.py

for win 7:
    cp ~/Documents/GitHub/PyHouse/src/plugins/nevow/plugins/pyhouse_location.py   /c/Python27/lib/site-packages/nevow/plugins/pyhouse_location.py

"""
from twisted.python import util
from nevow import athena
import PyHouse
#import PyHouse.src

pyhouseJsPackage = athena.AutoJSPackage(util.sibpath(PyHouse.__file__, 'src/web/js'))
pyhouseCssPackage = athena.AutoCSSPackage(util.sibpath(PyHouse.__file__, 'src/web/css'))
print "Plugin loaded..."

# ## END DBK
