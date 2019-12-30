"""
@name:      Modules/House/Family/insteon/insteon_link.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   Handle the all-link database(s) in Insteon devices.

This will maintain the all-link database in all Insteon devices.

Invoked periodically and when any Insteon device changes.
"""

__updated__ = '2019-12-26'

#  Import system type stuff
from typing import Optional

#  Import PyMh files
from Modules.Core.Utilities import convert
from Modules.House.Family.insteon.insteon_device import InsteonInformation
from Modules.House.Family.insteon.insteon_constants import ACK
from Modules.House.Family.insteon import insteon_utils
from Modules.House.Family.insteon.insteon_utils import Decode as utilDecode

from Modules.Core.Utilities.debug_tools import PrettyFormatAny, FormatBytes

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_link   ')


class LinkData():
    """
    """

    def __init__(self) -> None:
        self.Address: int = 123456  #  3 bytes
        self.Control: int = 0x0000  #  2 Bytes
        self.Data: str = '00.00.00'  #  3 bytes
        self.Flag: int = 0xC2
        self.Group: int = 0
        self._IsController: bool = False
        self._InsteonAddress: str = '12.34.56'
        self._Name: str = ''
        self._Type: str = 'Unknown'
        self._SubType: str = 'Unknown'


class Commands:
    """
    """

    def initiate_linking_as_controller(self, p_group=None):
        """
        Puts the PLM into linking mode as a controller.
        If p_group is specified the controller will be added for this group, otherwise it will be for group 00.
        =cut

        sub initiate_linking_as_controller {
            my ( $self, $group, $success_callback, $failure_callback ) = @_;
            $group = '00' unless $group;
            # set up the PLM as the responder
            my $cmd = '01';    # controller code
            $cmd .= $group;    # WARN - must be 2 digits and in hex!!
            my $message = new Insteon::InsteonMessage( 'all_link_start', $self );
            $message->interface_data($cmd);
            $message->success_callback($success_callback);
            $message->failure_callback($failure_callback);
            $self->queue_message($message);
        }
        """

    def initiate_unlinking_as_controller(self, p_group=None):
        """
        Puts the PLM into unlinking mode, if p_group is specified the PLM will try
        to unlink any devices linked to that group that identify themselves with a set
        button press.
        =cut

        sub initiate_unlinking_as_controller {
            my ( $self, $group ) = @_;
            $group = 'FF' unless $group;
            # set up the PLM as the responder
            my $cmd = 'FF';    # controller code
            $cmd .= $group;    # WARN - must be 2 digits and in hex!!
            my $message = new Insteon::InsteonMessage( 'all_link_start', $self );
            $message->interface_data($cmd);
            $self->queue_message($message);
        }
        """

    def cancel_linking(self):
        """
        Cancels any pending linking session that has not completed.
        =cut

        sub cancel_linking {
            my ($self) = @_;
            $self->queue_message( new Insteon::InsteonMessage( 'all_link_cancel', $self ) );
        }
        """

    def _get_aldb(self):
        """
        Returns the PLM's aldb object.
        =cut

        sub _aldb {
            my ($self) = @_;
            return $$self{aldb};
        }
        """


class SendCmd():
    """
    """

    def queue_0x62_command(self, p_controller_obj):
        """
        See p 231(244) of 2009 developers guide.
        See p 149(162) of 2009 developers guide.
        """
        # LOG.debug(PrettyFormatAny.form(p_controller_obj, 'Controller'))
        l_command = bytearray(22)
        l_command[0] = 0x02
        l_command[1] = 0x62
        insteon_utils.insert_address_into_message(p_controller_obj.Family.Address, l_command, 2)
        l_command[5] = 0x1F  #  Message Flags - Extended cmd
        l_command[6] = 0x2F  #  Cmd1
        l_command[7] = 0x01  #  Cmd2
        l_command[8] = 0x00  #  D1  Unused
        l_command[9] = 0x00  #  D2  Record request
        l_command[10] = 0x0F  # D3  High Byte
        l_command[11] = 0xF8  # D4  Low Byte
        l_command[12] = 0x01  # D5  All Records
        insteon_utils.queue_command(p_controller_obj, l_command, 'Query ALDB')

    def XXXqueue_0x67_command(self, p_controller_obj):
        """Reset the PLM (2 bytes)
        Puts the IM into the factory reset state which clears the All-Link Database.
        See p 255(268) of 2009 developers guide.
        """
        LOG.info("Queue command to reset the PLM (67).")
        l_command = insteon_utils.create_command_message('plm_reset')
        insteon_utils.queue_command(p_controller_obj, l_command, 'Reset PLM')

    def queue_0x69_command(self, p_controller_obj):
        """Get the first all-link record from the plm (2 bytes).
        See p 248(261) of 2009 developers guide.
        """
        LOG.info("Command to get First all-link record (0x69).")
        l_command = insteon_utils.create_command_message('plm_first_all_link')
        insteon_utils.queue_command(p_controller_obj, l_command, 'First All-Link')

    def queue_0x6A_command(self, p_controller_obj):
        """Get the next all-link record from the plm (2 bytes).
        See p 249(262) of 2009 developers guide.
        """
        LOG.info("Command to get the next all-link record (0x6A).")
        l_command = insteon_utils.create_command_message('plm_next_all_link')
        insteon_utils.queue_command(p_controller_obj, l_command, 'Next All-Link')

    def queue_0x6F_command(self, p_controller_obj, p_light_obj, p_code, p_flag, p_data):
        """Manage All-Link Record (11 bytes)
         See p 252(265) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6F
        [2] = Control Code
        [3] = All-Link record flag
        [4] = All-Link ecord group
        [5-7] = 3 Byte Link to address
        [8] = Data
        [9] = Data
        [10] = Data
       """
        LOG.info("Command to manage all-link record (6F).")
        l_command = insteon_utils.create_command_message('manage_all_link_record')
        l_command[2] = p_code
        l_command[3] = p_flag
        l_command[4] = p_light_obj.GroupNumber
        insteon_utils.insert_address_into_message(p_light_obj.Family.Address, l_command, 5)
        l_command[8:11] = p_data
        insteon_utils.queue_command(p_controller_obj, l_command, 'Manage ALDB record')

    def read_aldb_v2(self, p_controller_obj):
        """
        See p 231(244) of 2009 developers guide.
        See p 149(162) of 2009 developers guide.
        """
        self.queue_0x62_command(p_controller_obj)


class DecodeLink:
    """
    """
    m_pyhouse_obj = None
    m_controller_obj = None

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj

    """
            # More PLM ALDB Messages (Again should these be here???)
            if (   $record_type eq $prefix{all_link_first_rec}  # 0x69
                or $record_type eq $prefix{all_link_next_rec} ) {  # 0x6A
                # both of these conditions are ok as it just means we've reached the end of the memory
                $$self{_next_link_ok} = 0;
                $$self{_mem_activity} = undef;
                if ( $record_type eq $prefix{all_link_first_rec} ) {
                    $self->_aldb->health("empty");
                }
                else {
                    $self->_aldb->health("unchanged");
                }
                $self->_aldb->scandatetime(&main::get_tickcount);
                &::print_log( "[Insteon_PLM] " . $self->get_object_name . " completed link memory scan. Status: " . $self->_aldb->health() )
                  if $self->debuglevel( 1, 'insteon' );
                if ( $$self{_mem_callback} ) {
                    my $callback = $$self{_mem_callback};
                    $$self{_mem_callback} = undef;

                    package main;
                    eval($callback);
                    &::print_log( "[Insteon_PLM] WARN1: Error encountered during nack callback: " . $@ )
                      if $@ and $self->debuglevel( 1, 'insteon' );

                    package Insteon_PLM;
                }
            }

            elsif ( $record_type eq $prefix{all_link_send} ) {  # 0x61
                &::print_log( "[Insteon_PLM] WARN: PLM ALDB does not have a link for this scene defined: " . $pending_message->to_string . $@ );
            }

            elsif ( $record_type eq $prefix{all_link_start} ) {  # 0x64
                &::print_log( "[Insteon_PLM] WARN: PLM unable to enter linking mode: " . $pending_message->to_string . $@ );
            }

            elsif ( $record_type eq $prefix{all_link_manage_rec} ) {  # 0x6F
                # parse out the data
                my $failed_cmd_code = substr( $pending_message->interface_data(), 0, 2 );
                my $failed_cmd = 'unknown';
                if ( $failed_cmd_code eq '40' ) {
                    $failed_cmd = 'update/add controller record';
                }
                elsif ( $failed_cmd_code eq '41' ) {
                    $failed_cmd = 'update/add responder record';
                }
                elsif ( $failed_cmd_code eq '80' ) {
                    $failed_cmd = 'delete record';
                }
                my $failed_group    = substr( $pending_message->interface_data(), 4, 2 );
                my $failed_deviceid = substr( $pending_message->interface_data(), 6, 6 );
                &::print_log( "[Insteon_PLM] WARN: PLM unable to complete requested "
                      . "PLM link table update ($failed_cmd) for "
                      . "group: $failed_group and deviceid: $failed_deviceid" );
                my $callback;
                if ( $self->_aldb->{_success_callback} ) {
                    $callback = $self->_aldb->{_success_callback};
                    $self->_aldb->{_success_callback} = undef;
                }
                elsif ( $$self{_mem_callback} ) {
                    $callback = $pending_message->callback();    #$$self{_mem_callback};
                    $$self{_mem_callback} = undef;
                }
                if ($callback) {
                    package main;
                    eval($callback);
                    &::print_log( "[Insteon_PLM] WARN1: Error encountered during ack callback: " . $@ )
                      if $@ and $self->debuglevel( 1, 'insteon' );
                    package Insteon_PLM;
                }
            } else {
                &::print_log( "[Insteon_PLM] WARN: received NACK from PLM for " . $pending_message->to_string() );
            }
            $data =~ s/^$nackcmd//;
        }
    """

    def decode_0x53(self, p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 247(260) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x53
        [2] = LinkCode - 0=PLM is Responder, 1=PLM is Controller, FF=Deleted
        [3] = LinkGroup
        [4-6] = from address
        [7-8] = Dev Cat
        [9] = Firmwear Version


        elsif ( $record_type eq $prefix{all_link_complete} and ( length($data) >= 20 ) ) {  # 0x53
            #ALL-Linking Completed
            my $message_data = substr( $data, 4, 16 );
            ::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) )
              if $self->debuglevel( 4, 'insteon' );
            my $link_address = substr( $message_data, 4, 6 );
            ::print_log("[Insteon_PLM] DEBUG2: ALL-Linking Completed with $link_address ($message_data)") if $self->debuglevel( 2, 'insteon' );
            my $device_object = Insteon::get_object($link_address);
            $device_object->devcat( substr( $message_data, 10, 4 ) );
            $device_object->firmware( substr( $message_data, 14, 2 ) );
            #Insert the record into MH cache of the PLM's link table
            my $data1 = substr( $device_object->devcat, 0, 2 );
            my $data2 = substr( $device_object->devcat, 2, 2 );
            my $data3 = $device_object->firmware;
            my $type  = substr( $message_data,          0, 2 );
            my $group = substr( $message_data,          2, 2 );
            #Select type of link (00 - responder, 01 - master, ff - delete)
            if ( $type eq '00' ) {
                $self->_aldb->add_link_to_hash( 'A2', $group, '0', $link_address, $data1, $data2, $data3 );
            } elsif ( $type eq '01' ) {
                $self->_aldb->add_link_to_hash( 'E2', $group, '1', $link_address, $data1, $data2, $data3 );
            } elsif ( lc($type) eq 'ff' ) {
                # This is a delete request.
                # The problem is that the message from the PLM
                # does not identify whether the link deleted was
                # a responder or controller.  We could guess, b/c
                # it is unlikely that d1-d3 would be identical.
                # However, that seems sloppy.  For the time being
                # simply mark PLM aldb as unhealthy, and move on.
                if ( ref $self->active_message && $self->active_message->success_callback ) {
                    # This is LIKELY a delete in response to a MH
                    # request.  This is a bad way to check for
                    # this, but not sure what else to do.
                    # As a result, don't change health status
                } else {
                    $self->_aldb->health('changed');
                }
            }
            #Run success callback if it exists
            if ( ref $self->active_message ) {
                if ( $self->active_message->success_callback ) {
                    main::print_log( "[Insteon::Insteon_PLM] DEBUG4: Now calling message success callback: " . $self->active_message->success_callback )
                      if $self->debuglevel( 4, 'insteon' );
                    package main;
                    eval $self->active_message->success_callback;
                    ::print_log("[Insteon::Insteon_PLM] problem w/ success callback: $@") if $@;
                    package Insteon::BaseObject;
                }
                #Clear awaiting_ack flag
                $self->active_message->setby->_process_command_stack(0);
                $self->clear_active_message();
            }
            $data = substr( $data, 20 );
        }
        """
        l_message = p_controller_obj._Message
        l_msg = insteon_utils.decode_link_code(l_message[2])
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        l_device_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_from_id)
        utilDecode._devcat(l_message[7:9], p_controller_obj)
        _l_version = l_message[9]
        LOG.info('All-Link completed - Link Code:{}, Group:{}, From:{} '.format(l_msg, l_link_group, l_device_obj.Name))

    def decode_0x54(self, p_controller_obj):
        """Insteon Button Press event (3 bytes).
        The PLM set button was pressed.
        See p 263(276) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x54
        [2] = Button Event
        """
        l_message = p_controller_obj._Message
        l_event = l_message[2]
        LOG.info('The Set button was pressed {}'.format(l_event))

    def decode_0x55(self, p_controller_obj):
        """Insteon Reset Detected. (2 bytes)
        See p 256(269) of 2009 developers guide.

        Reports that the user manually put the IM into factory default state.
        Takes about 20 seconds to respond.

        [0] = 0x02
        [1] = 0x55
        """
        _l_message = p_controller_obj._Message
        LOG.info('The Set button was pressed')

    def decode_0x56(self, p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 243(256) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x56
        [2] = 0x01
        [3] = LinkGroup
        [4-6] = from address


        elsif ( $record_type eq $prefix{all_link_clean_failed} and ( length($data) >= 12 ) ) {  # 0x56
            #ALL-Link Cleanup Failure Report
            my $message_data = substr( $data, 4, 8 );
            if ( $self->active_message ) {
                # extract out the pertinent parts of the message for display purposes
                # bytes 0-1 - group; 2-7 device address
                my $failure_group  = substr( $message_data, 0, 2 );
                my $failure_device = substr( $message_data, 2, 6 );
                my $failed_object = &Insteon::get_object( $failure_device, '01' );
                if ( ref $failed_object ) {
                    ::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) )
                      if $failed_object->debuglevel( 4, 'insteon' );
                    ::print_log( "[Insteon_PLM] DEBUG2: Received all-link cleanup failure from "
                          . $failed_object->get_object_name
                          . " for all link group: $failure_group. Trying a direct cleanup." )
                      if $failed_object->debuglevel( 2, 'insteon' );
                    my $message = new Insteon::InsteonMessage( 'all_link_direct_cleanup', $failed_object, $self->active_message->command, $failure_group );
                    push( @{ $$failed_object{command_stack} }, $message );
                    $failed_object->_process_command_stack();
                }
                else {
                    ::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) )
                      if $self->debuglevel( 4, 'insteon' );
                    ::print_log( "[Insteon_PLM] Received all-link cleanup failure from an unkown device id: "
                          . "$failure_device and for all link group: $failure_group. You may "
                          . "want to run delete orphans to remove this link from your PLM" );
                }
            } else {
                ::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) )
                  if $self->debuglevel( 4, 'insteon' );
                ::print_log( "[Insteon_PLM] DEBUG2: Received all-link cleanup failure." . " But there is no pending message." )
                  if $self->debuglevel( 2, 'insteon' );
            }
            $data = substr( $data, 12 );
        }
        """
        l_message = p_controller_obj._Message
        l_link_code = l_message[2]
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        LOG.warning('All-Link-Clean failed {}, Group:{}, From:{} '.format(l_link_code, l_link_group, l_from_id))

    def decode_0x57(self, p_controller_obj):
        """ All-Link Record Response (10 bytes).
        See p 251(264) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x57
        [2] = AllLink Record Flags
        [3] = AllLink Group
        [4-6] = from address
        [7] = Link Data 1
        [8] = Link Data 2
        [9] = Link Data 3

        @param p_controller_obj: ==> ControllerInformation()

        elsif ( $record_type eq $prefix{all_link_record} and ( length($data) >= 20 ) ) {  # 0x57
            # Note Receipt of PLM Response
            $pending_message->plm_receipt(1);
            # ALL-Link Record Response
            my $message_data = substr( $data, 4, 16 );
            &::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) ) if $self->debuglevel( 4, 'insteon' );
            &::print_log("[Insteon_PLM] DEBUG2: ALL-Link Record Response:$message_data") if $self->debuglevel( 2, 'insteon' );
            $self->_aldb->parse_alllink($message_data);
            # before doing the next, make sure that the pending command (if it sitll exists) is pulled from the queue
            $self->clear_active_message();
            $self->_aldb->get_next_alllink();
            $data = substr( $data, 20 );
        }
        """
        l_message = p_controller_obj._Message[:10]
        l_link_obj = LinkData()
        l_link_obj.Flag = l_flags = l_message[2]
        l_link_obj.Group = l_group = l_message[3]
        l_link_obj._InsteonAddress = insteon_utils.extract_address_from_message(l_message, offset=4)
        l_link_obj.Data = l_data = [l_message[7], l_message[8], l_message[9]]
        l_flag_control = l_flags & 0x40
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
            l_link_obj._IsController = True
        l_addr = l_message[4:7]
        try:
            l_device_obj = utilDecode().get_obj_from_message(self.m_pyhouse_obj, l_addr)
            l_link_obj.Address = l_device_obj.Family.Address
            l_link_obj._Name = l_device_obj.Name
            l_link_obj._Type = l_device_obj.DeviceType
            l_link_obj._SubType = l_device_obj.DeviceSubType
        except:
            l_link_obj.Address = FormatBytes(l_addr)
            # l_key = 'Addr_{:#02X}.{:#02X}.{:#02X}'.format(l_message[4], l_message[5], l_message[6])
        l_key = len(p_controller_obj.LinkList)
        p_controller_obj.LinkList[l_key] = l_link_obj
        LOG.info('All-Link response-0x57 - Group={:#02X}, Name={}, Flags={:#x}, Data={}, {}'.format(l_group, l_device_obj.Name, l_flags, l_data, l_type))
        # LOG.debug(PrettyFormatAny.form(p_controller_obj, 'Controller'))
        for l_link in p_controller_obj.LinkList.values():
            LOG.debug(PrettyFormatAny.form(l_link, 'Links'))
        # Ask for next record
        SendCmd().queue_0x6A_command(p_controller_obj)

        return

    def decode_0x58(self, p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 242(255) of 2007 developers guide.


        elsif ( $record_type eq $prefix{all_link_clean_status} and ( length($data) >= 6 ) ) {  # 0x58
            #ALL-Link Cleanup Status Report
            my $message_data = substr( $data, 4, 2 );
            ::print_log( "[Insteon_PLM] DEBUG4:\n" . Insteon::MessageDecoder::plm_decode($data) )
              if $self->debuglevel( 4, 'insteon' );
            my $cleanup_ack = substr( $message_data, 0, 2 );
            if ( ref $self->active_message ) {
                if ( $cleanup_ack eq '15' ) {
                    &::print_log( "[Insteon_PLM] WARN1: All-link cleanup failure for scene: "
                          . $self->active_message->setby->get_object_name
                          . ". Retrying in 1 second." )
                      if $self->active_message->setby->debuglevel( 1, 'insteon' );
                    # except that we should cause a bit of a delay to let things settle out
                    $self->_set_timeout( 'xmit', 1000 );
                    $process_next_command = 0;
                } else {
                    my $message_to_string =
                      ( $self->active_message )
                      ? $self->active_message->to_string()
                      : "";
                    &::print_log("[Insteon_PLM] Received all-link cleanup success: $message_to_string")
                      if $self->active_message->setby->debuglevel( 1, 'insteon' );
                    if (   ref $self->active_message && ref $self->active_message->setby ) {
                        my $object = $self->active_message->setby;
                        $object->is_acknowledged(1);
                        $object->_process_command_stack();
                    }
                    $self->clear_active_message();
                }
            }
            $data = substr( $data, 6 );
        }
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Link-Clean-Status cleanup {}, Group:{}, From:{} '.format(l_status))

    def decode_0x64(self, p_controller_obj):
        """Start All-Link ACK response (5 bytes).
        See p 243(256) of 2007 developers guide.


        elsif ( $record_type eq $prefix{all_link_start} ) {  # 0x64
            if ( $self->active_message->success_callback ) {
                package main;
                eval( $self->active_message->success_callback );
                &::print_log( "[Insteon_PLM] WARN1: Error encountered during ack callback: " . $@ )
                  if ( $@
                    && $self->active_message->can('setby')
                    && ref $self->active_message->setby
                    && $self->active_message->setby->debuglevel( 1, 'insteon' ) );
                package Insteon_PLM;
            }
            # clear the active message because we're done
            $self->clear_active_message();
        }
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_ack = l_message[4]
        LOG.info("All-Link-Start  Ack - Group:{}, Cmd:{}, Ack:{}".format(l_grp, l_cmd1, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            LOG.error("== 64 - No ACK - Got {:#x}".format(l_ack))
            l_ret = False
        return l_ret

    def decode_0x65(self, p_controller_obj):
        """All-Link Cancel response (5 bytes).
        See p 244(257) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Link-Cancel {}, Group:{}, From:{} '.format(l_status))
        return False

    def decode_0x69(self, p_controller_obj):
        """Get All-Link First Record response (5 bytes).
        See p 248(261) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x69
        [2] = ACK/NAK


        if (   $record_type eq $prefix{all_link_first_rec}  # 0x69
            or $record_type eq $prefix{all_link_next_rec} ) {  # 0x6A
            $$self{_next_link_ok} = 1;
        }
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ack = 'ACK'
            # SendCmd().queue_0x6A_command(p_controller_obj)
        else:
            LOG.info("All-Link first record - NAK")
            l_ack = 'NAK'
        LOG.info("All-Link first record -{}".format(l_ack))
        return

    def decode_0x6A(self, p_controller_obj):
        """All-Link Next Record response (3 bytes).
        See p 249(262) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6A
        [2] = ACK/NAK


        if (   $record_type eq $prefix{all_link_first_rec}  # 0x69
            or $record_type eq $prefix{all_link_next_rec} ) {  # 0x6A
            $$self{_next_link_ok} = 1;
        }
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ack = 'ACK'
            # SendCmd().queue_0x6A_command(p_controller_obj)
        else:
            l_ack = 'NAK'
        LOG.info("All-Link Next record - {}".format(l_ack))
        return

    def decode_0x6C(self, p_controller_obj):
        """All-Link Record for sender response (3 bytes).
        See p 250(263) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6C
        [2] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        LOG.info("All-Link Record for sender record - ACK")
        if l_message[2] == ACK:
            l_ret = True
        else:
            LOG.info("All-Link Record for sender record - NAK")
            l_ret = False
        return l_ret

    def decode_0x6f(self):
        """
        elsif ( $record_type eq $prefix{all_link_manage_rec} ) {  # 0x6F
            # Managing the PLM's ALDB
            $self->clear_active_message();
            my $callback;
            if ( $self->_aldb->{_success_callback} ) {
                $callback = $self->_aldb->{_success_callback};
                $self->_aldb->{_success_callback} = undef;
            }
            elsif ( $$self{_mem_callback} ) {
                $callback = $pending_message->callback();    #$$self{_mem_callback};
                $$self{_mem_callback} = undef;
            }
            if ($callback) {
                package main;
                eval($callback);
                &::print_log( "[Insteon_PLM] WARN1: Error encountered during ack callback: " . $@ )
                  if ( $@
                    && $self->active_message->can('setby')
                    && ref $self->active_message->setby
                    && $self->active_message->setby->debuglevel( 1, 'insteon' ) );
                package Insteon_PLM;
            }
            }
        """


class InsteonAllLinks:

    def get_all_allinks(self, p_controller_obj):
        """A command to fetch the all-link database from the PLM
        """
        LOG.info("Get all All-Links from controller {}.".format(p_controller_obj.Name))

        SendCmd().queue_0x69_command(p_controller_obj)
        # SendCmd().read_aldb_v2(p_controller_obj)
        # Send.queue

    """
    Reviews the cached version of all of the ALDBs and, based on this review, removes
    links from this device which are not present in the mht file, not defined in the
    code, or links which are only half-links..

    =cut

    sub delete_orphan_links {
        my ( $self, $audit_mode ) = @_;

        &::print_log("[Insteon::ALDB_PLM] #### NOW BEGINNING DELETE ORPHAN LINKS ####");
        @{ $$self{_delete_device_failures} } = ();
        $self->SUPER::delete_orphan_links($audit_mode);
        # iterate over all registered objects and compare whether the link tables match defined scene linkages in known Insteon_Links
        for my $obj ( &Insteon::find_members('Insteon::BaseDevice') ) {
            #Match on real objects only
            if ( ( $obj->is_root ) ) {
                my %delete_req = ( 'root_object' => $obj, 'audit_mode' => $audit_mode );
                push @{ $$self{delete_queue} }, \%delete_req;
            }
        }
        $self->_process_delete_queue();
    }
    """

    """
    sub _process_delete_queue {
        my ( $self, $p_num_deleted ) = @_;
        $$self{delete_queue_processed} += $p_num_deleted if $p_num_deleted;
        my $num_in_queue = @{ $$self{delete_queue} };
        if ($num_in_queue) {
            my $delete_req_ptr   = shift( @{ $$self{delete_queue} } );
            my %delete_req       = %$delete_req_ptr;
            my $failure_callback = $$self{device}->get_object_name . "->_aldb->_process_delete_queue_failure";
            # distinguish between deleting PLM links and processing delete orphans for a root item
            if ( $delete_req{'root_object'} ) {
                $$self{current_delete_device} = $delete_req{'root_object'}->get_object_name;
                my $is_batch_mode = 1;
                $delete_req{'root_object'}->delete_orphan_links( ( $delete_req{'audit_mode'} ) ? 1 : 0, $failure_callback, $is_batch_mode );
            }
            else {
                $$self{current_delete_device} = $$self{device}->get_object_name;
                &::print_log(
                    "[Insteon::ALDB_PLM] now deleting orphaned link w/ details: "
                      . (
                        ( $delete_req{is_controller} ) ? "controller($delete_req{data3})"
                        : "responder"
                      )
                      . ", "
                      . (
                        ( $delete_req{object} ) ? "object=" . $delete_req{object}->get_object_name
                        : "deviceid=$delete_req{deviceid}"
                      )
                      . ", group=$delete_req{group}"
                ) if $self->{device}->debuglevel( 1, 'insteon' );
                $delete_req{failure_callback} = $failure_callback;
                $self->delete_link(%delete_req);
                $$self{delete_queue_processed}++;
            }
        }
        else {
            ::print_log("[Insteon::ALDB_PLM] Delete All Links has Completed.");
            my $_delete_failure_cnt = scalar $$self{_delete_device_failures};
            if ($_delete_failure_cnt) {
                my $obj_list;
                for my $failed_obj ( @{ $$self{_delete_device_failures} } ) {
                    $obj_list .= $failed_obj . ", ";
                }
                ::print_log( "[Insteon::ALDB_PLM] However, some failures were " . "noted with the following devices: $obj_list" );
            }
            ::print_log("[Insteon::ALDB_PLM] A total of $$self{delete_queue_processed} orphaned link records were deleted.");
            ::print_log("[Insteon::ALDB_PLM] #### END DELETE ORPHAN LINKS ####");
        }
    }

    sub _process_delete_queue_failure {
        my ($self) = @_;
        push @{ $$self{_delete_device_failures} }, $$self{current_delete_device};
        ::print_log( "[Insteon::ALDB_PLM] WARN: failure occurred when deleting orphan links from: " . $$self{current_delete_device} . ".  Moving on..." );
        $self->health('changed');
        $self->_process_delete_queue;

    }
    """

    """
    Deletes a specific link from a device.  Generally called by C<delete_orphan_links()>.

    =cut

    sub delete_link {
        # linkkey is concat of: deviceid, group, is_controller
        my ( $self, $parms_text ) = @_;
        my %link_parms;
        if ( @_ > 2 ) {
            shift @_;
            %link_parms = @_;
        }
        else {
            %link_parms = &main::parse_func_parms($parms_text);
        }
        my $num_deleted    = 0;
        my $insteon_object = $link_parms{object};
        my $deviceid       = ($insteon_object) ? $insteon_object->device_id : $link_parms{deviceid};
        my $group          = $link_parms{group};
        my $is_controller  = ( $link_parms{is_controller} ) ? 1 : 0;
        my $subaddress     = ( defined $link_parms{data3} ) ? $link_parms{data3} : '00';
        my $linkkey        = $self->get_linkkey( $deviceid, $group, $is_controller, $subaddress );
        if ( defined $$self{aldb}{$linkkey} ) {
            my $cmd = '80'
              . $$self{aldb}{$linkkey}{flags}
              . $$self{aldb}{$linkkey}{group}
              . $$self{aldb}{$linkkey}{deviceid}
              . $$self{aldb}{$linkkey}{data1}
              . $$self{aldb}{$linkkey}{data2}
              . $$self{aldb}{$linkkey}{data3};
            delete $$self{aldb}{$linkkey};
            $num_deleted = 1;
            my $message = new Insteon::InsteonMessage( 'all_link_manage_rec', $$self{device} );
            $$self{_success_callback} = ( $link_parms{callback} ) ? $link_parms{callback} : undef;
            $$self{_failure_callback} = ( $link_parms{failure_callback} ) ? $link_parms{failure_callback} : undef;
            $message->interface_data($cmd);
            $$self{device}->queue_message($message);
        }
        else {
            &::print_log( "[Insteon::ALDB_PLM] no entry in linktable could be found for: "
                  . "deviceid=$deviceid, group=$group, is_controller=$is_controller, subaddress=$subaddress" );
            if ( $link_parms{callback} ) {
                package main;
                eval( $link_parms{callback} );
                &::print_log( "[Insteon_PLM] error in add link callback: " . $@ )
                  if $@ and $self->{device}->debuglevel( 1, 'insteon' );
                package Insteon_PLM;
            }
        }
        return $num_deleted;
    }
    """

    """
    Adds the link to the device's ALDB.  Generally called from the "sync links" or "link to interface" voice commands.
    =cut

    sub add_link {
        my ( $self, $parms_text ) = @_;
        my %link_parms;
        if ( @_ > 2 ) {
            shift @_;
            %link_parms = @_;
        }
        else {
            %link_parms = &main::parse_func_parms($parms_text);
        }
        my $device_id;
        my $group = ( $link_parms{group} ) ? $link_parms{group} : '01';
        my $insteon_object = $link_parms{object};
        if ( !( defined($insteon_object) ) ) {
            $device_id = lc $link_parms{deviceid};
            $insteon_object = &Insteon::get_object( $device_id, $group );
        }
        else {
            $device_id = lc $insteon_object->device_id;
        }
        my $is_controller = ( $link_parms{is_controller} ) ? 1 : 0;
        my $subaddress = ( defined $link_parms{data3} ) ? $link_parms{data3} : '00';
        my $linkkey = $self->get_linkkey( $device_id, $group, $is_controller, $subaddress );
        if ( defined $$self{aldb}{$linkkey} ) {
            &::print_log( "[Insteon::ALDB_PLM] WARN: attempt to add link to PLM that already exists! "
                  . "deviceid=$device_id, group=$group, is_controller=$is_controller, subaddress=$subaddress" );
            if ( $link_parms{callback} ) {
                package main;
                eval( $link_parms{callback} );
                &::print_log( "[Insteon::ALDB_PLM] error in add link callback: " . $@ )
                  if $@ and $self->{device}->debuglevel( 1, 'insteon' );
                package Insteon_PLM;
            }
        }
        else {
            # The modem developers guide appears to be wrong regarding control codes.
            # 40 and 41 will respond with a NACK if a record for that group/device/is_controller combination already exist.
            # It appears that code 20 can be used to edit existing but not create new records.
            # However, since data1-3 are consistent for all PLM links we never really need to update a PLM link.
            # NB prior MH code did not set data3 on control records to the group, however this does not appear to have any adverse effects,
            #  and the current MH code will not flag these entries as being incorrect or requiring an update.
            my $control_code = ($is_controller) ? '40' : '41';
            # flags should be 'a2' for responder and 'e2' for controller
            my $flags = ($is_controller) ? 'E2' : 'A2';
            my $data1 =
              ( defined $link_parms{data1} )
              ? $link_parms{data1}
              : ( ($is_controller) ? '01' : '00' );
            my $data2 = ( defined $link_parms{data2} ) ? $link_parms{data2} : '00';
            my $data3 = ( defined $link_parms{data3} ) ? $link_parms{data3} : '00';
            # from looking at manually linked records, data1 and data2 are both 00 for responder records
            # and, data1 is 01 and usually data2 is 00 for controller records
            my $cmd = $control_code . $flags . $group . $device_id . $data1 . $data2 . $data3;
            $$self{aldb}{$linkkey}{flags}         = lc $flags;
            $$self{aldb}{$linkkey}{group}         = lc $group;
            $$self{aldb}{$linkkey}{is_controller} = $is_controller;
            $$self{aldb}{$linkkey}{deviceid}      = lc $device_id;
            $$self{aldb}{$linkkey}{data1}         = lc $data1;
            $$self{aldb}{$linkkey}{data2}         = lc $data2;
            $$self{aldb}{$linkkey}{data3}         = lc $data3;
            $$self{aldb}{$linkkey}{inuse}         = 1;
            $self->health('unchanged') if ( $self->health() eq 'empty' );
            my $message = new Insteon::InsteonMessage( 'all_link_manage_rec', $$self{device} );
            $message->interface_data($cmd);
            $$self{_success_callback} =
              ( $link_parms{callback} ) ? $link_parms{callback} : undef;
            $$self{_failure_callback} =
              ( $link_parms{failure_callback} )
              ? $link_parms{failure_callback}
              : undef;
            $message->interface_data($cmd);
            $$self{device}->queue_message($message);
        }
    }
    """

    """
    This is used in response to an all_link_complete command received by the PLM.
    This may be from the C<Insteon::BaseInterface::link_to_interface_i2cs> routine, or it may be as a result of a manual link creation
    This routine manually adds a record to MH's cache of the PLM ALDB.
    Normally you only want to add records during a scan of the ALDB, so use this routine with caution.

    =cut

    sub add_link_to_hash {
        my ( $self, $flags, $group, $is_controller, $device_id, $data1, $data2, $data3 ) = @_;
        my $linkkey = $self->get_linkkey( $device_id, $group, $is_controller, $data3 );
        $$self{aldb}{$linkkey}{flags}         = lc $flags;
        $$self{aldb}{$linkkey}{group}         = lc $group;
        $$self{aldb}{$linkkey}{is_controller} = $is_controller;
        $$self{aldb}{$linkkey}{deviceid}      = lc $device_id;
        $$self{aldb}{$linkkey}{data1}         = lc $data1;
        $$self{aldb}{$linkkey}{data2}         = lc $data2;
        $$self{aldb}{$linkkey}{data3}         = lc $data3;
        $$self{aldb}{$linkkey}{inuse}         = 1;
        $self->health('unchanged') if ( $self->health() eq 'empty' );
        return;
    }
    """

    """
    Checks and returns true if a link with the passed details exists on the device
    or false if it does not.  Generally called as part of C<delete_orphan_links()>.

    =cut

    sub has_link {
        my ( $self, $insteon_object, $group, $is_controller, $data3 ) = @_;
        my $key = $self->get_linkkey( $insteon_object->device_id, $group, $is_controller, $data3 );
        my $found = 0;
        $found++ if ( defined $$self{aldb}{$key} );
        return ($found);
    }
    """

    """
    """


class Api:
    """
    """

    def read_link(self):
        """
        """
        LOG.info('Reading Link xxx')

    def write_link(self):
        """
        """
        LOG.info('Writing Link xxx')

    def delete_link(self, p_controller_obj, p_address, p_group, p_flag):
        """Delete an all link record.
        """
        #  p_light_obj = LightData()
        p_light_obj = InsteonInformation()
        p_light_obj.InsteonAddress = convert.dotted_hex2int(p_address)
        p_light_obj.GroupNumber = p_group
        #  p_code = 0x00  # Find First
        p_code = 0x00  #  Delete First Found record
        #  p_flag = 0xE2
        p_data = bytearray(b'\x00\x00\x00')
        LOG.info("Delete All-link record - Address:{}, Group:{:#02X}".format(p_light_obj.InsteonAddress, p_group))
        l_ret = SendCmd().queue_0x6F_command(p_controller_obj, p_light_obj, p_code, p_flag, p_data)
        return l_ret

    def _x(self):
        _y = PrettyFormatAny.form(0, '')

#  ## END DBK
