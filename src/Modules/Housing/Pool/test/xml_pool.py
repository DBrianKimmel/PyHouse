"""
@name:      PyHouse/src/Modules/Housing/Pool/test/xml_pool.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 27, 2015
@Summary:

"""
__updated__ = '2017-01-13'

TESTING_POOL_SECTION = 'PoolSection'

L_POOL_SECTION_START = '<' + TESTING_POOL_SECTION + '>'
L_POOL_SECTION_END = '</' + TESTING_POOL_SECTION + '>'

TESTING_POOL_NAME_0 = 'Pond'
TESTING_POOL_KEY_0 = '0'
TESTING_POOL_ACTIVE_0 = 'True'
TESTING_POOL_UUID_0 = 'Pool....-0000-0000-0000-0123456789ab'
TESTING_POOL_COMMENT_0 = 'Pond with Lilly Pads'
TESTING_POOL_TYPE_0 = 'Pond'

L_POOL_START_0 = '  ' + \
        '<Pool Name="' + TESTING_POOL_NAME_0 + \
        '" Key="' + TESTING_POOL_KEY_0 + \
        '" Active="' + TESTING_POOL_ACTIVE_0 + '">'
L_POOL_UUID_0 = '<UUID>' + TESTING_POOL_UUID_0 + '</UUID>'
L_POOL_COMMENT_0 = '<Comment>' + TESTING_POOL_COMMENT_0 + '</Comment>'
L_POOL_TYPE_0 = '<PoolType>' + TESTING_POOL_TYPE_0 + '</PoolType>'

TESTING_POOL_NAME_1 = 'Hot Tub'
TESTING_POOL_KEY_1 = '1'
TESTING_POOL_ACTIVE_1 = 'True'
TESTING_POOL_UUID_1 = 'Pool....-0001-0001-0001-0123456789ab'
TESTING_POOL_COMMENT_1 = 'Year Round Hot Tub'
TESTING_POOL_TYPE_1 = 'HotTub'

L_POOL_START_1 = '<Pool Name="' + TESTING_POOL_NAME_1 + '" Key="' + TESTING_POOL_KEY_1 + '" Active="' + TESTING_POOL_ACTIVE_1 + '">'
L_POOL_UUID_1 = '<UUID>' + TESTING_POOL_UUID_1 + '</UUID>'
L_POOL_COMMENT_1 = '<Comment>' + TESTING_POOL_COMMENT_1 + '</Comment>'
L_POOL_TYPE_1 = '<PoolType>' + TESTING_POOL_TYPE_1 + '</PoolType>'
L_POOL_END = '</Pool>'

L_POOL_0 = '\n'.join([
    L_POOL_START_0,
    L_POOL_UUID_0,
    L_POOL_COMMENT_0,
    L_POOL_TYPE_0,
    L_POOL_END
])

L_POOL_1 = '\n'.join([
    L_POOL_START_1,
    L_POOL_UUID_1,
    L_POOL_COMMENT_1,
    L_POOL_TYPE_1,
    L_POOL_END
])

XML_POOL = '\n'.join([
    L_POOL_SECTION_START,
    L_POOL_0,
    L_POOL_1,
    L_POOL_SECTION_END
])

# ## END DBK
