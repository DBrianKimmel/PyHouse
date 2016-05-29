"""
@name:      PyHouse/src/Modules/Communication/test/xml_communications.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""


L_COMMUNICATION_START = '<CommunicationSection>'
L_COMMUNICATION_END = '</CommunicationSection>'

L_EMAIL_START = '<EmailSection>'
L_EMAIL_END = '</EmailSection>'

L_TWITTER_START = '<TwitterSection>'
L_TWITTER_END = '</TwitterSection>'

XML_EMAIL = """
    <EmailSection>
        <EmailFromAddress>mail.sender@Gmail.Com</EmailFromAddress>
        <EmailToAddress>mail.receiver@Gmail.Com</EmailToAddress>
        <GmailLogin>TestAccount@Gmail.Com</GmailLogin>
        <GmailPassword>Test=!=Password</GmailPassword>
    </EmailSection>
    <CommunicationSection>
    </CommunicationSection>
"""


TESTING_CONSUMER_KEY = 'ABCDEFGHIJKLKMNOPQRSTUVWXYZ'
TESTING_CONSUMER_SECRET = '1234567890ABCDEFGHIJKLKMNOPQRSTUVWXYZ'
TESTING_ACCESS_TOKEN = 'ZYXWVUTSRQPONMLKJIHFEDCBA'
TESTING_ACCESS_TOKEN_SECRET = '0987654321ZYXWVUTSRQPONMLKJIHFEDCBA'

L_CONSUMER_KEY = '    <ConsumerKey>' + TESTING_CONSUMER_KEY + '</ConsumerKey>'
L_CONSUMER_SECRET = '    <ConsumerSecret>' + TESTING_CONSUMER_SECRET + '</ConsumerSecret>'


XML_TWITTER = '\n'.join([
    L_TWITTER_START,
    L_TWITTER_END
])

XML_COMMUNICATION = '\n'.join([
    L_COMMUNICATION_START,
    XML_EMAIL,
    XML_TWITTER,
    L_COMMUNICATION_END
])

# ## END DBK
