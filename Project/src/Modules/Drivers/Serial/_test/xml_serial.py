"""
@name:      PyHouse/Project/src/Modules/Drivers/Serial/_test/xml_serial.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 9, 2014
@Summary:

"""

__updated__ = '2019-06-09'

TESTING_SERIAL_BAUD_RATE = '19200'
TESTING_SERIAL_BYTE_SIZE = '8'
TESTING_SERIAL_PARITY = 'N'
TESTING_SERIAL_STOP_BITS = '1.0'
TESTING_SERIAL_TIMEOUT = '1.0'
TESTING_SERIAL_DSR_DTR = 'False'
TESTING_SERIAL_RTS_CTS = 'False'
TESTING_SERIAL_XON_XOFF = 'False'

L_BAUD = '<BaudRate>' + TESTING_SERIAL_BAUD_RATE + '</BaudRate>'
L_BYTE_SIZE = '<ByteSize>' + TESTING_SERIAL_BYTE_SIZE + '</ByteSize>'
L_PARITY = '<Parity>' + TESTING_SERIAL_PARITY + '</Parity>'
L_STOP_BITS = '<StopBits>' + TESTING_SERIAL_STOP_BITS + '</StopBits>'
L_TIMEOUT = '<Timeout>' + TESTING_SERIAL_TIMEOUT + '</Timeout>'
L_DSR_DTR = '<DsrDtr>' + TESTING_SERIAL_DSR_DTR + '</DsrDtr>'
L_RTS_CTS = '<RtsCts>' + TESTING_SERIAL_RTS_CTS + '</RtsCts>'
L_XON_XOFF = '<XonXoff>' + TESTING_SERIAL_XON_XOFF + '</XonXoff>'

XML_SERIAL = '\n'.join([
    "<Serial>",
    L_BAUD,
    L_BYTE_SIZE,
    L_PARITY,
    L_STOP_BITS,
    L_TIMEOUT,
    L_DSR_DTR,
    L_RTS_CTS,
    L_XON_XOFF,
    "</Serial>"
])

# ## END DBK
