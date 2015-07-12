"""
@name:      PyHouse/src/Modules/Web/test/xml_web.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

If PasswordMethod is "UNIX" then the password is fetched from the system.
"""


WEB_SERVER_XML = """
    <WebSection>
        <WebPort>8580</WebPort>
        <LoginSection>
            <Login Active="True" Key="0" Name="briank">
                <PasswordMethod>UNIX</PasswordMethod>
                <Password>123456789</Password>
                <FullName>D. Brian Kimmel</FullName>
            </Login>
        </LoginSection>
    </WebSection>
"""



# ## END DBK
