#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import logging
import Queue

# Import PyMh files
#import configure_mh
import Device_UPB
from tools import PrintBytes



# UPB Control Word
# Page 15
LINK_PKT = 0x80
LOW_REQ = 0x02

ACK_REQ = 0x10
ACK_ID = 0x20
ACK_MSG = 0x40

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3

g_debug = 0
g_driver = []
g_logger = None
g_queue = None
g_reactor = None

m_logger = None

pim_commands = {
'start_setup_mode'          : 0x03,
'stop_setup_mode'           : 0x04,
'get_device_status'         : 0x07,
'get_register_value'        : 0x10,
'set_register_value'        : 0x11,
'goto'                      : 0x22,
'fade_start'                : 0x23,
'fade_stop'                 : 0x24,
'report_state'              : 0x30,
}


Controller_Data = Device_UPB.Controller_Data

g_network_id = 0
g_unit_id = 0xFF
g_controller = []


class PimData(object):
    """Locally held data about each of the PIM controllers we find.
    """

    def __init__(self):
        self.Name = None
        self.NetworkID = 0
        self.UnitID = 0xFF
        self.Interface = None
        self.Password = None

class UpbPimUtility(object):

    def _get_id_from_name(self, p_name):
        if g_debug > 1: print " & UPB_Pim._get_id_from_name ", p_name
        for l_obj in Device_UPB.Light_Data.itervalues():
            if l_obj.Family != 'UPB': continue
            if l_obj.Active != True: continue
            if l_obj.Name == p_name:
                l_unit_id = int(l_obj.UnitID)
                return l_unit_id
        for l_obj in Device_UPB.Controller_Data.itervalues():
            if l_obj.Family != 'UPB': continue
            if l_obj.Active != True: continue
            if l_obj.Name == p_name:
                l_unit_id = int(l_obj.UnitID)
                return l_unit_id
        return 0

    def _calculate_checksum(self, p_msg):
        if g_debug > 1: print " & UPB_Pim.calculate checksum"
        l_out = '14'
        l_cs = 0
        for l_ix in range(len(p_msg)):
            l_byte = p_msg[l_ix]
            l_cs = (l_cs + l_byte) % 256
            l_out = "{0:}{1:02X}".format(l_out, l_byte)
        l_out = "{0:}{1:02X}0D".format(l_out, int(256 - l_cs))
        return l_out
    """
    for ( int l_ix = 0; l_ix < k_array.size(); l_ix++ ) {
        l_byte = k_array[l_ix]&0xFF;
        l_cs = ( l_cs + l_byte ) % 256;
        if ( l_byte < 0x10 )
            l_out.append( '0' );
        l_out.append( QByteArray().setNum( l_byte, 16 ) );
    }
    l_out.append( QByteArray().setNum( 256 - l_cs, 16 ) );
    l_out.append( 0x0d );
    """

    def _compose_command(self, p_command, p_device_id, *p_args):
        """
        """
        if g_debug > 1: print " & UPB_Pim.compose command - Network:{0:}, Command:{1:#02x}, ID:{2:} ".format(g_network_id, p_command, p_device_id)
        l_cmd = bytearray(6 + len(p_args))
        l_cmd[0] = 7 + len(p_args) # 'UPBMSG_CONTROL_HIGH'
        l_cmd[1] = 0x00 # 'UPBMSG_CONTROL_LOW'
        l_cmd[2] = g_network_id # 'UPBMSG_NETWORK_ID'
        l_cmd[3] = p_device_id # 'UPBMSG_DEST_ID'
        l_cmd[4] = g_unit_id # 'UPBMSG_SOURCE_ID'
        l_cmd[5] = p_command # 'UPBMSG_MESSAGE_ID'
        for l_ix in range(len(p_args)):
            #print "   ", (6 + l_ix), p_args[l_ix]
            l_cmd[6 + l_ix] = p_args[l_ix]
        l_cmd = self._calculate_checksum(l_cmd)
        self.send_pim_command(l_cmd)
        return l_cmd


class PimDriverInterface(object):

    def driver_loop_start(self):
        if g_debug > 0: print "--- UPB PIM DriverLoopStart"
        g_reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send)
        g_reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop)

    def send_pim_command(self, p_command):
        print " & UPB_Pim.send_pim_command ", p_command
        g_queue.put(p_command)

    def dequeue_and_send(self):
        try:
            l_command = g_queue.get(False)
        except  Queue.Empty:
            g_reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send)
            return
        try:
            print " dequeue_and_send ", l_command
            g_driver[0].write_device(l_command)
            #for l_ix in range(len(l_command)):
            #    g_driver[0].write_device(l_command[l_ix])
        except IOError:
            pass
        except IndexError: # No controller defined so [0] will be invalid
            pass
        g_reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send)

    def receive_loop(self):
        try:
            (l_bytes, l_msg) = g_driver[0].fetch_read_data()
        except IndexError:
            (l_bytes, l_msg) = (0, '')
        if l_bytes == 0:
            g_reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop)
            return False
        #l_ret = self._decode_message(l_msg, l_bytes)
        l_ret = l_msg
        g_reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop)
        return l_ret


class CreateCommands(UpbPimUtility, PimDriverInterface):
    """
    """

    def set_register_value(self, p_name, p_register, p_values):
        """Set one of the device's registers.
        """
        print " & UPB_Pim.set_register_value - Name:{0:}, Register:{1:02X}, Values:{2:}".format(p_name, p_register, p_values)
        self._compose_command(pim_commands['set_register_value'], self._get_id_from_name(p_name), int(p_register), p_values[0])
        pass

    def set_pim_mode(self):
        l_val = bytearray(1)
        l_val[0] = 0x03
        self.set_register_value(self.m_pim_name[0], 0x70, l_val)

class LightingAPI(Device_UPB.LightingAPI, CreateCommands):

    def change_light_setting(self, p_name, p_level):
        for l_obj in Device_UPB.Light_Data.itervalues():
            if l_obj.get_family() != 'UPB': continue
            if l_obj.get_active() == False: continue
            if l_obj.get_name() == p_name:
                l_id = self._get_id_from_name(p_name)
                print " & UPB_Pim.change_light_settings "
                g_logger.info('change_light_setting()')
                l_cmd = self._compose_command(pim_commands['goto'], l_id, p_level, 0x01)
                self.send_pim_command(l_cmd)
                return

    def update_all_devices(self):
        #Device_Insteon.InsteonLightingAPI.update_all_devices(Device_Insteon.InsteonLightingAPI())
        pass

class LightHandlerAPI(LightingAPI):
    """This is the API for light control.
    """

class DecodeResponses(CreateCommands): pass

class UpbPimAPI(CreateCommands):

    def initialize_all_controllers(self):
        """Find and initialize all UPB PIM type controllers.
        """
        global g_network_id, g_unit_id
        l_count = 0
        for l_key, l_obj in Device_UPB.Controller_Data.iteritems():
            if l_obj.Family.lower() != 'upb': continue
            if l_obj.Active != True: continue
            #
            l_pim = PimData()
            l_pim.Name = l_obj.Name
            l_interface = l_obj.Interface
            g_network_id = l_obj.NetworkID
            g_logger.info('Found UPB PIM named: {0:}, Type={1:}'.format(l_pim.Name, l_interface))
            print " & UPB_Pim.initialize_all_controllers - Loading: ", l_key
            g_network_id = l_obj.NetworkID
            g_unit_id = int(l_obj.UnitID)
            if l_obj.Interface.lower() == 'serial':
                import drivers.Driver_Serial
                l_driver = drivers.Driver_Serial.SerialDriverMain(l_obj)
            elif l_obj.Interface.lower() == 'ethernet':
                import drivers.Driver_Ethernet
                l_driver = drivers.Driver_Ethernet.EthernetDriverMain(l_obj)
            elif l_obj.Interface.lower() == 'usb':
                import drivers.Driver_USB
                l_driver = drivers.Driver_USB.USBDriverMain(l_obj)
            else:
                g_logger.error("UPB PIM has no known interface type! {0}, {1:}".format(l_obj.get_name, l_obj.get_interface))
            g_driver.append(l_driver)
            self.initialize_one_controller(l_driver, l_obj)
            l_count += 1
        g_logger.info("Loaded {0:} UPB_PIM controllers".format(l_count))

    def initialize_one_controller(self, _p_driver, p_obj):
        """Do whatever it takes to set the controller up for working on the UPB network.
        Send a write register 70 to set PIM mode
        Command is <17>70 03 8D <0D>
        """
        self.set_register_value(p_obj.get_name(), 0x70, [0x03])

    def send_pim_command_get_response(self, p_command):
        print " & PIM.send_pim_command_get_response ", p_command
        g_logger.info('Sending command {0:}'.format(PrintBytes(p_command)))
        g_driver[0].write_device(g_driver[0], p_command)
        _l_ret = None
        # Pim should always get a PA for getting the message to send.
        _l_ret = self.get_response()
        # if the remote light device got a good message we should get an ack next.
        l_ret = self.get_response()
        return l_ret

    def get_response(self):
        pass

    """ int PIMMain::getResponse( QByteArray& kr_msg ) {
    QByteArray  l_response, l_qba, l_decoded;
    int l_ret = receiveLong( l_response );
    l_ret = decodeResponse( l_response, l_decoded );
    kr_msg = l_decoded;
    return l_ret;
}
    """
    """ int PIMMain::receiveShort( QByteArray& kr_msg ) {
    int l_ret = -1;
    if ( m_interface == PIM_USB ) {
        l_ret = mp_pimUsbPort->usbReadBytes( kr_msg );
        DEBUG( 8, "PIMMain::receiveShort (USB) - Len" << kr_msg.size() );
    } else {
        DEBUG( 0, "PIMMain::receiveShort - ERROR invalid pim type=" << m_interface );
    }
    return l_ret;
}
    """
    """ int PIMMain::receiveLong( QByteArray& kr_msg ) {
    QByteArray l_qba, l_response;
    int l_ret = receiveShort( l_qba );
    int l_len = l_qba[0] & 0x0F;
    int l_repeat = 40;
    // First a (hopefully) short spin to see if data is ready.
    while ( l_len == 0 && l_repeat > 0 ) {
        usleep( 20000 );
        l_ret = receiveShort( l_qba );
        l_len = l_qba[0] & 0x0F;
        l_repeat--;
    }
    // Next - get all the data.
    l_len = l_qba[0] & 0x0F;
    l_repeat = 50;
    while ( l_len != 0 && l_repeat > 0 ) {
        l_qba.remove( 0, 1 ); // Drop the length encoded byte
        l_response.append( l_qba );
        l_ret = receiveShort( l_qba );
        l_len = l_qba[0] & 0x0F;
        l_repeat--;
    }
    // We should have the whole message by now.
    if ( l_response.size() > 0 ) {
        QString l_str = messageToString( l_response );
        DEBUG( 1, "PIMMain::receiveLong " << l_str.toAscii() );
    }
    kr_msg = l_response;
    return l_response.size();
}
    """


class PimTesting(UpbPimAPI): pass


def Init():
    global g_logger, g_queue
    g_logger = logging.getLogger('PyHouse.UPB_PIM')
    g_logger.info('Initializing.')
    g_queue = Queue.Queue(300)
    UpbPimAPI().initialize_all_controllers()
    g_logger.info('Initialized.')

def Start(p_reactor):
    global g_reactor
    g_logger.info('Starting.')
    g_reactor = p_reactor
    PimDriverInterface().driver_loop_start()

def Stop():
    pass




    """
//< Offsets into a UPB message
const int UPBMSG_CONTROL_HIGH = 0;
const int UPBMSG_CONTROL_LOW  = 1;
const int UPBMSG_NETWORK_ID   = 2;
const int UPBMSG_DEST_ID      = 3;
const int UPBMSG_SOURCE_ID    = 4;
const int UPBMSG_MESSAGE_ID   = 5;
const int UPBMSG_BODY         = 6;

// Commands to the pim
const int CMD_START_SETUP_MODE          = 0x03;
const int CMD_STOP_SETUP_MODE           = 0x04;
const int CMD_GET_DEVICE_STATUS         = 0x07;
const int CMD_GET_REGISTER_VALUE        = 0x10;
const int CMD_SET_REGISTER_VALUE        = 0x11;
const int CMD_GOTO                      = 0x22;
const int CMD_FADE_START                = 0x23;
const int CMD_FADE_STOP                 = 0x24;
const int CMD_REPORT_STATE              = 0x30;

PIMMain::PIMMain(int k_debug, QObject* kp_parent ) :
        mp_parent( kp_parent ) {
    m_pimConfigured = FALSE;
    m_isOpen = FALSE;
    mp_pimUsbPort    = new UsbPort( PIM_USB_VENDOR_ID, PIM_USB_PRODUCT_ID, m_debugLevel );
    m_interface = PIM_USB;
    // Temp values
    m_netID             = 0xFF;
    m_unitID            = 255;
    pimConfigure();
    mp_nextTimer   = new QTimer();
    QObject::connect( mp_nextTimer, SIGNAL( timeout() ), this, SLOT( slotTimer() ) );
    QObject::connect( this, SIGNAL( signalPimRxed( QByteArray ) ), this, SLOT( slotReceivedPimMessage( QByteArray ) ) );
    mp_nextTimer->start( 1*1000 );
}
    """
    """
Erc_t PIMMain::pimOpen( const QString& k_portName, const QString& k_controllerName, const QString& k_interface) {
    m_portName = k_portName;
    m_controllerName = k_controllerName;
    if ( k_interface == "SERIAL" ) {
        m_interface = PIM_SERIAL;
    } else if ( k_interface == "USB" ) {
        m_interface = PIM_USB;
    } else {
        m_interface = PIM_INVALID;
    }
    m_pimConfigured = FALSE;
    if ( m_interface == PIM_SERIAL ) {
        return ERC_OK;
    } else if ( m_interface == PIM_USB ) {
        // Send a write register 70 to set PIM mode
        // Command is <17>70 03 8D <0D>
        QByteArray l_msg( 1, 0x03 );
        pimWriteRegisters( 0x70, l_msg );
        m_isOpen = TRUE;
        mp_nextTimer->stop();
        mp_nextTimer->start( 1*1000 );
        DEBUG( -2, "PIMMain::pimOpen - USB - Exit OK" );
        return ERC_OK;
    }
    // Something we do not know about then.
    m_isOpen = FALSE;
    return ERC_SERVICE_NOT_AVAIL;
}

Erc_t PIMMain::pimClose() {
    DEBUG( 1, "PIMMain::pimClose()" );
    return ERC_OK;
}

bool PIMMain::pimReOpen() {
    DEBUG( 1, "PIMMain::pimReOpen" );
    pimClose();
    pimOpen();
    return TRUE;
}
    """
    """
QByteArray PIMMain::pimReadRegisters( int k_regStart, int k_count ) {
    QByteArray  l_msg( 2, 0 );
    QByteArray  l_response;
    DEBUG( -1, "PIMMain::pimReadRegisters()" );
    // Build PIM comand to read its internal registers.
    l_msg[0] = k_regStart & 0xFF;
    l_msg[1] = k_count & 0xFF;
    pimCalculateCS( l_msg );
    l_msg.prepend( 0x12 );
    slotPimSendMessage( l_msg );
    getResponse( l_response );  // PA
    return l_response;
}

int PIMMain::pimWriteRegisters( int k_regStart, QByteArray& k_values ) {
    QByteArray  l_msg;
    QByteArray  l_response;
    DEBUG( -1, "PIMMain::pimWriteRegisters start=" << k_regStart << " Count=" << k_values.size() );
    l_msg = k_values;
    l_msg.prepend( k_regStart );
    pimCalculateCS( l_msg );
    l_msg.prepend( 0x17 );
    slotPimSendMessage( l_msg );
    getResponse( l_response );   // PA
    DEBUG( -2, "PIMMain::pimWriteRegisters - Exit" );
    return 0;
}
    """
    """
QByteArray PIMMain::pimDetectNetworks() {
    QByteArray  l_msg, l_answer;
    QByteArray  l_response;
    DEBUG( -1, "PIMMain::pimDetectNetworks" );
    for ( int l_ix = 1; l_ix < 25; l_ix++ ) {
        l_msg = QByteArray( 6, 0 );
        DEBUG( 1, "PIMMain::pimDetectNetworks net=" << l_ix);
        l_msg[UPBMSG_CONTROL_HIGH] = 1;
        l_msg[UPBMSG_CONTROL_LOW]  = 0x10; // Request ack and acknowledgement
        l_msg[UPBMSG_NETWORK_ID]   = l_ix & 0xFF;
        l_msg[UPBMSG_DEST_ID]      = 0x00; // Broadcast DID
        l_msg[UPBMSG_SOURCE_ID]    = m_unitID & 0xFF;
        l_msg[UPBMSG_MESSAGE_ID]   = 0x00 & 0xFF; // aka messageID
        l_msg[UPBMSG_CONTROL_HIGH] = ( l_msg.size() + 1 ) & 0xFF;
        pimCalculateCS( l_msg );
        l_msg.prepend( 0x14 );
        slotPimSendMessage( l_msg );
        int l_net = getResponse( l_response );   // PA
        if ( l_net == 1 ) {
            l_answer.append( (char)l_ix );
        }
    }
    QString l_str = messageToString( l_answer, FALSE );
    DEBUG( 1, "=========== " << l_answer.size() << " " << l_str.toAscii() );
    m_debugLevel = 0;
    return l_answer;
}
    """
    """
QByteArray PIMMain::ScanDevices(int k_net, int k_min, int k_max) {
    QByteArray l_out, l_answer, l_response;
    for ( int l_ix = k_min; l_ix < k_max; l_ix++ ) {
        l_out = QByteArray( 6, 0 );
        DEBUG( -1, "PIMMain::ScanDevices " << l_ix);
        l_out[UPBMSG_CONTROL_LOW]  = 0x10;
        l_out[UPBMSG_NETWORK_ID]   = k_net & 0xFF;
        l_out[UPBMSG_DEST_ID]      = l_ix & 0xFF;
        l_out[UPBMSG_SOURCE_ID]    = m_unitID & 0xFF;
        l_out[UPBMSG_MESSAGE_ID]   = CMD_GET_DEVICE_STATUS & 0xFF;
        l_out[UPBMSG_CONTROL_HIGH] = ( ( l_out.size() + 1 ) ) & 0xFF;
        pimCalculateCS( l_out );
        DEBUG( 5, "PIMMain::ScanDevices - TRANSMIT_UPB_MESSAGE" << l_out.data() );
        l_out.prepend( 0x14 );
        slotPimSendMessage( l_out );
        int l_net = getResponse( l_response );   // PA
        DEBUG( -1, "PIMMain::ScanDevices " << l_ix << " Responded " << l_net);
        if ( l_net < 4 ) {
            l_answer.append( (char)l_ix );
        }
        sleep(3);
    }
    QString l_str = messageToString( l_answer, FALSE );
    DEBUG( -1, "=====PIMMain::ScanDevices found " << l_answer.size() << " Devices, UnitIDs are " << l_str.toAscii() );
    return l_answer;
}

int PIMMain::pimGetNetworkInfo(  LightDevice* kp_device, QByteArray& k_nameRet ) {
    QByteArray l_out, l_response;
    bool l_ok;
    getDeviceRegisterReport( kp_device, 0, 1, l_response );
    int l_netID = l_response.toInt( &l_ok, 16 );
    getDeviceRegisterReport( kp_device, 16, 16, l_response );
    for ( int l_ix = 0; l_ix < 16; l_ix++ ) {
        QByteArray l_char = l_response.left( 2 );
        l_response.remove( 0, 2 );
        l_out[l_ix] = (char)( l_char.toInt( &l_ok, 16 ) );
    }
    if (  m_debugLevel > 0 ) {
        QString l_str = messageToString( l_out );
        DEBUG( 1, "PIMMain::pimGetNetworkInfo name=" << l_str << l_netID );
    }
    k_nameRet = l_out;
    return l_netID;
}
    """
    """
void PIMMain::ProgramDeviceInSetup( LightDevice* kp_device ) {
    // These are what we want to program into the device - so build the proper array.
    int l_unitID    = kp_device->property( "UnitID" ).toInt();
    int l_netID     = kp_device->property( "NetworkID" ).toInt();
    int l_password  = kp_device->property( "Password" ).toInt();
    // temp patch - Ugly hack alert !!!
    l_netID = 6;
    l_password = 0x050D;
    QByteArray l_out( 4, 0 );
    l_out[0] = l_netID & 0xFF;
    l_out[1] = l_unitID & 0xFF;
    l_out[2] = ( l_password / 256 ) & 0xFF;
    l_out[3] = ( l_password % 256 ) & 0xFF;
    QString l_str   = QString("%1").arg(l_password,4,16, QLatin1Char( '0' ));
    DEBUG( -1, "PIMMain::ProgramDeviceInSetup -to- New UnitID=" << l_unitID << ", new netID=" << l_netID << ", New Password=" << l_str );
    // temp patch - Ugly hack alert !!!
    l_netID = 6;
    l_password = 0x050D;
    // These are the factory defaults of the device.
    // We need to send the message to this address so it will see the new program params.
    // This ws where the above message will be sent by setting up kp_device.
    kp_device->setProperty( "UnitID", 0x00 );
    kp_device->setProperty( "NetworkID", 0x00 );
    kp_device->setProperty( "Password", 0x1234 );
    // Write the NetworkID, UnitID and NetworkPassword
    writeDeviceRegisters( kp_device, 0, 4, l_out );
    // Update the LightDevice to what we just programmed.
    kp_device->setProperty( "UnitID", l_unitID );
    kp_device->setProperty( "NetworkID", l_netID );
    kp_device->setProperty( "Password", l_password );
    exitSetupMode( kp_device );
    DEBUG( -2, "PIMMain::ProgramDeviceInSetup - Exit" );
    m_debugLevel = 0;
}
    """
    """
int PIMMain::getDeviceRegisterReport( LightDevice* kp_device, int k_start, int k_count, QByteArray& k_value ) {
    QByteArray  l_response;
    DEBUG( 1, "PIMMain::getDeviceRegisterReport  start=" << k_start << ", Count=" << k_count );
    if ( ( k_count < 1 ) || ( k_count > 16 ) ) {
        DEBUG( 0, "PIMMain::getDeviceRegisterReport count not 1 to 16 =" << k_count );
        return -1;
    }
    QByteArray      l_out( 2, (char)0 );
    l_out[0] = k_start & 0xFF;
    l_out[1] = k_count & 0x1F;
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_GET_REGISTER_VALUE, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
    getResponse( l_response );   // PU
    if ( ( l_response.size() - 14 ) != ( k_count * 2 ) ) {
        DEBUG( 0, "PIMMain::getDeviceRegisterReport - ERROR invalid report recieved" );
        return -1;
    }
    l_response = decodeReport( l_response );
    k_value = l_response;
    return k_count;
}

int PIMMain::writeDeviceRegisters( LightDevice* kp_device, int k_start, int k_count, QByteArray& k_value ) {
    if ( k_value.size() != k_count ) {
        DEBUG( 0, "PIMMain::writeDeviceRegisters size mismatch " << k_count <<  k_value.size() );
    }
    QString l_str = "";
    for ( int l_ix= 0; l_ix < k_count; l_ix++ ) {
        l_str += QString("%1 ").arg(k_value[l_ix], 2,16, QLatin1Char( '0' ));
    }
    QByteArray  l_response;
    DEBUG( -1, "PIMMain::writeDeviceRegisters  start=" << k_start << ", Count=" << k_count << l_str );
    QByteArray l_out = k_value;
    l_out.prepend( k_start & 0xFF );
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_SET_REGISTER_VALUE, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
    DEBUG( -2, "PIMMain::writeDeviceRegisters - Exit" );
    return 0;
}
    """
    """
bool PIMMain::getDeviceInfo( LightDevice* kp_device ) {
    QString l_name = kp_device->property( "DeviceName" ).toString();
    QByteArray  l_response;
    bool l_ok;
    DEBUG( -1, "PIMMain::getDeviceInfo for device" << l_name.toAscii() );
    // Network
    getDeviceRegisterReport( kp_device, 0, 1, l_response );
    int l_netID = l_response.toInt( &l_ok, 16 );
    // Unit ID
    getDeviceRegisterReport( kp_device, 1, 1, l_response );
    int l_unitID = l_response.toInt( &l_ok, 16 );
    int l_mfgrID, l_prodID;
    getMfgrProduct(kp_device,l_mfgrID,l_prodID);
    kp_device->setProperty( "Mfgr", l_mfgrID );
    kp_device->setProperty( "Product", l_prodID );
    DEBUG( -1, "PIMMain::getDeviceInfo for " << l_name.toAscii() << ", UnitID=" << l_unitID << ", NetID=" << l_netID
            << ", MfgrID=" << l_mfgrID << ", ProductID=" << l_prodID );
    return TRUE;
}

bool PIMMain::getMfgrProduct( LightDevice* kp_device, int& k_mfgrRet, int& k_productRet ) {
    QByteArray  l_response;
    bool l_ok;
    DEBUG( 1, "PIMMain::getMfgrProduct" );
    getDeviceRegisterReport( kp_device, 6, 2, l_response );
    int l_mfgrID = l_response.toInt( &l_ok, 16 );
    getDeviceRegisterReport( kp_device, 8, 2, l_response );
    int l_prodID = l_response.toInt( &l_ok, 16 );
    k_mfgrRet = l_mfgrID;
    k_productRet = l_prodID;
    return TRUE;
}

int PIMMain::pimGetDeviceStateReport( LightDevice* kp_device ) {
    QByteArray l_response;
    bool l_ok;
    DEBUG( 1, "PIMMain::pimGetDeviceStateReport" );
    QByteArray      l_out( 2, (char)0 );
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_REPORT_STATE, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
    getResponse( l_response );   // PU
    // All I have seen so far is a one byte result which is the
    //  the light level 0x00 thru 0x64 (0-100).
    l_response = decodeReport( l_response );
    int l_value = l_response.toInt( &l_ok, 16 );
    return l_value;
}

void PIMMain::pimGetDeviceStatusReport( LightDevice* kp_device ) {
    QByteArray  l_out, l_response;
    DEBUG( 1, "PIMMain::pimGetDeviceStatusReport" );
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_GET_DEVICE_STATUS, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
    getResponse( l_response );   // PU
    l_response = decodeReport( l_response );
}

bool PIMMain::pimIsValid() {
    DEBUG( 1, "PIMMain::pimIsValid - Bool=" << m_isOpen );
    return TRUE; // m_isOpen;
}

    """
    """
// Protected methods.

QByteArray PIMMain::pimComposeMessage( LightDevice* kp_device, int k_cmd, QByteArray k_values, bool k_link ) {
    QByteArray l_out( 6, 0 );
    int l_unitID = kp_device->property( "UnitID" ).toInt();
    int l_netID  = kp_device->property( "NetworkID" ).toInt();
    DEBUG( 1, "PIMMain::pimComposeMessage UnitID=" << l_unitID << " cmd=" << k_cmd << " Len=" << k_values.size() << " NetID=" << l_netID );
    l_out[UPBMSG_CONTROL_LOW]  = 0x10;
    l_out[UPBMSG_NETWORK_ID]   = l_netID & 0xFF;
    l_out[UPBMSG_DEST_ID]      = l_unitID & 0xFF;
    l_out[UPBMSG_SOURCE_ID]    = m_unitID & 0xFF; // aka messageID
    l_out[UPBMSG_MESSAGE_ID]   = k_cmd & 0xFF; // aka messageID
    l_out.append( k_values );
    l_out[UPBMSG_CONTROL_HIGH] = ( ( l_out.size() + 1 ) ) & 0xFF;
    // This is a link command so modify the control
    if ( k_link )
        l_out[UPBMSG_CONTROL_HIGH] = l_out[UPBMSG_CONTROL_HIGH] | 0x80;
    pimCalculateCS( l_out );
    DEBUG( 5, "PIMMain::pimComposeMessage TRANSMIT_UPB_MESSAGE" << l_out.data() );
    l_out.prepend( 0x14 );
    return l_out;
}

bool PIMMain::pimConfigure() {
    return TRUE;
}

    """
    """
// Private Methods

int PIMMain::decodeResponse( QByteArray& k_msg, QByteArray& k_msgRet ) {
    int         l_ret = 0;
    QByteArray  l_response = k_msg;
    int l_len = k_msg.size();
    QByteArray  l_reg;
    k_msgRet.clear();

    QString l_str = messageToString( k_msg );
    DEBUG( 7, "PIMMain::decodeResponse - Len=" << l_len << " " << l_str.toAscii() );
    // All pIM response messages begin with 'P' which is 0x50
    if ( l_response[0] != (char)0x50 ) {
        DEBUG( 1, "decodeResponse did not find valid message 1 - ERROR! char was " << (int)l_response[0] );
        l_response.remove( 0, 1 );
        l_len--;
        if ( l_len < 1 ) return -1;
    }
    while ( l_len > 0 ) {
        if ( l_response[0] == (char) 0x0D ) {
            l_response.remove( 0, 1 );
            l_len--;
            //l_ret = -1;
            continue;
        }
        if ( l_response[0] != (char)0x50 ) {
            DEBUG( 1, "decodeResponse did not find valid message 2 - ERROR! char was " << (int)l_response[0] );
            l_response.remove( 0, 1 );
            l_len--;
            l_ret = -1;
            continue;
        }
        switch( l_response[1] ) {
            case 0x41:      // 'A'
                DEBUG( 3, "... A - Message accepted." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x0001;
                break;
            case 0x45:      // 'E'
                DEBUG( -3, "... E - Rejected prev cmd because it contained an error." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8001;
                break;

            case 0x4B:      // 'K'
                DEBUG( 3, "... K - Ack pulse was also recieved." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x0002;
                break;
            case 0x4E:      // 'N'
                DEBUG( -3, "... N - NO ack pulse was recieved from device." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8002;
                break;

            case 0x42:      // 'B'
                DEBUG( -3, "... B - Rejected prev cmd because PIM is busy." );
                l_response.remove( 0, 3 );
                l_len -= 3;
                l_ret |= 0x8004;
                break;

            case 0x52:      // 'R'
                // get rid of 'PR'
                l_response.remove( 0, 2 ); l_len -= 2;
                // get register #
                l_reg =  l_response.left( 2 ); l_response.remove( 0, 2 ); l_len -= 2;
                // we now have the registers values encoded as hex nibbles
                while ( l_response[0] != (char)0x0d ) {
                    k_msgRet.append( l_response[0] );
                    l_response.remove( 0, 1 );
                    l_len--;
                }
                DEBUG( 3, "... R - Register report recieved - Register=" << l_reg << " " << k_msgRet );
                l_ret |= 0x0010;
                break;

            case 0x55:      // 'U'
                l_response.remove( 0, 2 );
                l_len -= 2;
                l_reg =  l_response.left( 2 );
                l_response.remove( 0, 2 );
                l_len -= 2;
                while ( l_response[0] != (char)0x0d ) {
                    k_msgRet.append( l_response[0] );
                    l_response.remove( 0, 1 );
                    l_len--;
                }
                l_len--;
                DEBUG( -3, "... U - Message Report recieved - len=" << l_reg << "  " << k_msgRet << " Len-" << l_len );
                l_ret |= 0x0020;
                break;

            default:
                DEBUG( 0, "... Unhandled return message. len=" << l_len << " " << l_response );
                l_len--;
                l_response.remove( 0, 1 );
                l_ret |= 0x8100;
        }
    }
    return l_ret;
}

QByteArray PIMMain::decodeReport( const QByteArray& k_report ) {
    QByteArray l_report = k_report;
    // Get the network bytes.
    QByteArray l_netArr = l_report.left( 4 );
    l_report.remove( 0, 4 );
    // Get the UnitID bytes.
    QByteArray l_unitArr = l_report.left( 4 );
    l_report.remove( 0, 4 );
    // Get the report ID
    QByteArray l_reportArr = l_report.left( 2 );
    l_report.remove( 0, 2 );
    // Get the starting offset.
    QByteArray l_offsetArr = l_report.left( 2 );
    l_report.remove( 0, 2 );
    // Pick up the checksum from the end of the string.
    QByteArray l_cksumtArr = l_report.right( 2 );
    l_report.chop( 2 );
    DEBUG( 1, "PIMMain::decodeReport  Net=" << l_netArr << " Unit=" << l_unitArr \
                << " Report=" << l_reportArr << " Offset=" << l_offsetArr << "  Report=" << l_report );
    return l_report;
}

QString PIMMain::messageToString ( const QByteArray& k_ba, bool k_short ) {
    QString l_str( " " );
    char    l_char[8];
    int     l_size = k_ba.length();
    for ( int l_ix = 0; l_ix < l_size; l_ix++ ) {
        unsigned int l_ch = (unsigned int)k_ba[l_ix]&0xFF;
        unsigned int l_pch = l_ch;
        if ( l_ch < 0x20 || l_ch > 0x7f ) l_pch = 0x20;
        if ( k_short && ( ( l_ch >= 0x20 ) && ( l_ch <= 0x7f ) ) )
            sprintf( l_char, "%c ", (char)l_pch );
        else
            sprintf( l_char, "0x%2.2X ", l_ch );
        l_str.append( l_char );
    }
    return l_str;
}

void PIMMain::enterSetupMode( LightDevice* kp_device ) {
    QByteArray  l_response;
    int l_password  = 0x0d0a; // kp_device->getUPBDevicePointer()->getDeviceNetworkPointer()->getNetworkPassword();
    DEBUG( 1, "PIMMain::enterSetupMode" );
    QByteArray      l_out( 2, (char)0 );
    l_out[0] = ( l_password / 256 ) & 0xFF;
    l_out[1] = ( l_password % 256 ) & 0xFF;
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_START_SETUP_MODE, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
}

void PIMMain::exitSetupMode( LightDevice* kp_device ) {
    QByteArray  l_response, l_out;
    DEBUG( 1, "PIMMain::exitSetupMode " );
    QByteArray l_msg = pimComposeMessage( kp_device, CMD_STOP_SETUP_MODE, l_out, FALSE );
    sendMessageGetResponse(l_msg, l_response);
}

void PIMMain::decode89Report( const QByteArray& k_rept ) {
// turned on remote light fireplace
//QTime("17:31:36") PIMMain::slotReceivedPimMessage " P U 8 9 0 4 0 6 6 B 0 2 2 0 F F F F E 2 0x0D "
//QTime("17:31:37") PIMMain::slotReceivedPimMessage " P U 8 9 0 5 0 6 6 B 0 2 2 0 F F F F E 1 0x0D "
// turned off remote light - fireplace
//QTime("17:31:41") PIMMain::slotReceivedPimMessage " P U 8 9 0 4 0 6 6 C 0 2 2 1 F F F F E 0 0x0D "
//QTime("17:31:42") PIMMain::slotReceivedPimMessage " P U 8 9 0 5 0 6 6 C 0 2 2 1 F F F F D F 0x0D "
    QByteArray l_report = k_rept;
    DEBUG( 1, "PIMMain::decode89Report" );
    // the report ID = 89
    l_report.remove( 0, 2 );
    bool l_ok;
    // 2 bytes of something
    // perhape 04 = button pressed and 05 = button released
    int l_field1 = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of NetworkID = 06
    int l_netID = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of LinkID = 6B(107) and 6C(108)
    int l_linkID = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of something
    int l_field4 = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of command - 20=activate selected link, 21=deactivate selected link
    int l_field5 = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of something - FF
    int l_field6 = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    // 2 bytes of something - FF
    int l_field7 = l_report.left( 2 ).toInt( &l_ok, 16 );
    l_report.remove( 0, 2 );
    DEBUG( -2, "PIMMain::decode89Report field1=" << l_field1 << ", Net=" << l_netID << ", LinkID=" << l_linkID
            << ", field-4=" << l_field4 << ", DeviceCommand=" << l_field5 << ", field-6=" << l_field6 << ", field-7=" << l_field7 );
}
    """

### END
