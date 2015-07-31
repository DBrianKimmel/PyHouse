"""
@name:      PyHouse/src/Modules/Communication/test/xml_communications.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""


EMAIL_XML = """
    <EmailSection>
        <EmailFromAddress>mail.sender@Gmail.Com</EmailFromAddress>
        <EmailToAddress>mail.receiver@Gmail.Com</EmailToAddress>
        <GmailLogin>TestAccount@Gmail.Com</GmailLogin>
        <GmailPassword>Test=!=Password</GmailPassword>
    </EmailSection>
    <CommunicationSection>
    </CommunicationSection>
"""



XML_COMMUNICATION = '\n'.join([
    EMAIL_XML
])

# ## END DBK
