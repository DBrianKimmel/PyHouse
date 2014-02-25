"""
Created on Feb 21, 2014

@author: briank
"""

from twisted.trial import unittest


XML = """
<House Name='House_1' Key='0' Active='True'>
    <Controllers>
        <Controller Name='Serial_1' Key='0' Active='True'>
            <Comment>This is a comment for Serial_1</Comment>
            <Controller>True</Controller
            <Interface>Serial</Interface>
            <BaudRate>19200</BaudRate>
            <ByteSize>8</ByteSize>
            <DsrDtr>False</DsrDtr>
            <Parity>N</Parity>
            <RtsCts>False</RtsCts>
            <StopBits>1.0</StopBits>
            <Timeout>0</Timeout>
            <XonXoff>False</XonXoff>
        </Controller>
        <Controller Name='USB_1' Key='1' Active='True'>
            <Interface>USB</Interface>
            <Vendor>12345</Vendor>
            <Product>9876</Product>
        </Controller>
    </Controllers>
</House>
"""


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass

