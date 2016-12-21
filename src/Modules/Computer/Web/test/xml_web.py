"""
@name:      PyHouse/src/Modules/Web/test/xml_web.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 30, 2015
@Summary:

"""

__updated__ = '2016-11-22'

# Import system type stuff

# Import PyMh files


L_WEB_SECTION_START = '<WebSection>'
L_WEB_SECTION_END = '</WebSection>'
L_LOGIN_SECTION_START = '<LoginSection>'
L_LOGIN_SECTION_END = '</LoginSection>'
L_LOGIN_END = '</Login>'

TESTING_WEB_PORT = '8580'
TESTING_WEB_SECURE_PORT = '8588'

L_WEB_PORT = '    <Port>' + TESTING_WEB_PORT + '</Port>'
L_WEB_SECURE_PORT = '    <SecurePort>' + TESTING_WEB_SECURE_PORT + '</SecurePort>'

TESTING_LOGIN_NAME_0 = 'Admin-00'
TESTING_LOGIN_KEY_0 = '0'
TESTING_LOGIN_ACTIVE_0 = 'True'
TESTING_LOGIN_UUID_0 = 'Login...-0000-0000-0000-0123456789ab'
TESTING_LOGIN_FULL_NAME_0 = 'Administrator-00'
TESTING_LOGIN_PASSWORD_0 = 'ChangeMe'
TESTING_LOGIN_ROLE_0 = 'Admin'

L_LOGIN_START_0 = '      ' + \
    '<Login Name="' + TESTING_LOGIN_NAME_0 + \
    '" Key="' + TESTING_LOGIN_KEY_0 + \
    '" Active="' + TESTING_LOGIN_ACTIVE_0 + \
    '">'
L_LOGIN_UUID_0 = '<UUID>' + TESTING_LOGIN_UUID_0 + '</UUID>'
L_LOGIN_FULL_NAME_0 = '      <FullName>' + TESTING_LOGIN_FULL_NAME_0 + '</FullName>'
L_LOGIN_PASSWORD_0 = '      <Password>' + TESTING_LOGIN_PASSWORD_0 + '</Password>'
L_LOGIN_ROLE_0 = '      <Role>' + TESTING_LOGIN_ROLE_0 + '</Role>'

L_LOGIN_USER_0 = '\n'.join([
    L_LOGIN_START_0,
    L_LOGIN_UUID_0,
    L_LOGIN_FULL_NAME_0,
    L_LOGIN_PASSWORD_0,
    L_LOGIN_ROLE_0,
    L_LOGIN_END
])

TESTING_LOGIN_NAME_1 = 'User1'
TESTING_LOGIN_KEY_1 = '1'
TESTING_LOGIN_ACTIVE_1 = 'True'
TESTING_LOGIN_UUID_1 = 'Login...-0001-0001-0001-0123456789ab'
TESTING_LOGIN_FULL_NAME_1 = 'User One Name'
TESTING_LOGIN_PASSWORD_1 = 'Pass1'
TESTING_LOGIN_ROLE_1 = 'Adult'

L_LOGIN_START_1 = '      ' + \
    '<Login Name="' + TESTING_LOGIN_NAME_1 + \
    '" Key="' + TESTING_LOGIN_KEY_1 + \
    '" Active="' + TESTING_LOGIN_ACTIVE_1 + \
    '">'
L_LOGIN_UUID_1 = '<UUID>' + TESTING_LOGIN_UUID_1 + '</UUID>'
L_LOGIN_FULL_NAME_1 = '      <FullName>' + TESTING_LOGIN_FULL_NAME_1 + '</FullName>'
L_LOGIN_PASSWORD_1 = '      <Password>' + TESTING_LOGIN_PASSWORD_1 + '</Password>'
L_LOGIN_ROLE_1 = '      <Role>' + TESTING_LOGIN_ROLE_1 + '</Role>'
L_LOGIN_USER_1 = '\n'.join([
    L_LOGIN_START_1,
    L_LOGIN_UUID_1,
    L_LOGIN_FULL_NAME_1,
    L_LOGIN_PASSWORD_1,
    L_LOGIN_ROLE_1,
    L_LOGIN_END
])

XML_WEB_SERVER = '\n'.join([
    L_WEB_SECTION_START,
    L_WEB_PORT,
    L_WEB_SECURE_PORT,
    L_LOGIN_SECTION_START,
    L_LOGIN_USER_0,
    L_LOGIN_USER_1,
    L_LOGIN_SECTION_END,
    L_WEB_SECTION_END
    ])

# ## END DBK
