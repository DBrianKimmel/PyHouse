'''
Created on Sep 29, 2012

@author: briank
'''

import uuid as sys_uuid

class UUID(object):

    def __init__(self):
        self.uuid = 'uuid:' + str(sys_uuid.uuid1())
        #print("Created uuid = >>{0:}<<".format(self.uuid))

    def __repr__(self):
        return str(self.uuid)


