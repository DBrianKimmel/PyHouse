"""
name:       Modules/security/dropbox_uploader.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2019 by D. Brian Kimmel
@note:      Created on May 31, 2014
@license:   MIT License
@summary:   Gather this node's information.

"""


# from Modules.security.dropbox_uploader import ACCESS_LEVEL






ACCESS_LEVEL = "dropbox"
CURL_BIN = "/usr/bin/curl"
CURL_ACCEPT_CERTIFICATES = "-k"
CURL_PARAMETERS = "-s"







# Don't edit these...
API_REQUEST_TOKEN_URL = "https://api.dropbox.com/1/oauth/request_token"
API_USER_AUTH_URL = "https://www2.dropbox.com/1/oauth/authorize"
API_ACCESS_TOKEN_URL = "https://api.dropbox.com/1/oauth/access_token"
API_CHUNKED_UPLOAD_URL = "https://api-content.dropbox.com/1/chunked_upload"
API_CHUNKED_UPLOAD_COMMIT_URL = "https://api-content.dropbox.com/1/commit_chunked_upload"
API_UPLOAD_URL = "https://api-content.dropbox.com/1/files_put"
API_DOWNLOAD_URL = "https://api-content.dropbox.com/1/files"
API_DELETE_URL = "https://api.dropbox.com/1/fileops/delete"
API_MOVE_URL = "https://api.dropbox.com/1/fileops/move"
API_COPY_URL = "https://api.dropbox.com/1/fileops/copy"
API_METADATA_URL = "https://api.dropbox.com/1/metadata"
API_INFO_URL = "https://api.dropbox.com/1/account/info"
API_MKDIR_URL = "https://api.dropbox.com/1/fileops/create_folder"
API_SHARES_URL = "https://api.dropbox.com/1/shares"
APP_CREATE_URL = "https://www2.dropbox.com/developers/apps"
RESPONSE_FILE = "$TMP_DIR/du_resp_$RANDOM"
CHUNK_FILE = "$TMP_DIR/du_chunk_$RANDOM"








class Dropbox(object):

    def encode_auth(self, p_app_key, p_access_token, p_plaintext):
        l_ret = '?'
        l_ret += 'oauth_consumer_key=' + p_app_key
        l_ret += '&oauth_token=' + p_access_token
        l_ret += '&oauth_signature_method=' + p_plaintext
        # &oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET
        # &oauth_timestamp=$(utime)&oauth_nonce=$RANDOM
        return l_ret

    def simple_upload_file(self, p_source, p_dest):
# Simple file upload
# $1 = Local source file
# $2 = Remote destination file

        self.m_source = p_source
        self.m_dest = p_dest

        print(" > Uploading p_src to p_dest...")
        # $CURL_BIN $CURL_ACCEPT_CERTIFICATES $CURL_PARAMETERS -i --globoff -o "$RESPONSE_FILE" \
        #       --upload-file "$FILE_SRC" "$API_UPLOAD_URL/$ACCESS_LEVEL/$(urlencode "$FILE_DST") xxxxx"
        # check_http_response

        # Check
        # if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        #    print "DONE\n"
        # else
        #    print "FAILED\n"
        #    print "An error occurred requesting /upload\n"
        #    ERROR_STATUS=1
        # fi


    def _get_access_level(self):
        print(" # Permission type, App folder or Full Dropbox [a/f]: ")
        # read ACCESS_LEVEL
        ACCESS_LEVEL = ''

        if  ACCESS_LEVEL == "a":
            ACCESS_LEVEL = "sandbox"
            ACCESS_MSG = "App Folder"
        else:
            ACCESS_LEVEL = "dropbox"
            ACCESS_MSG = "Full Dropbox"





























# import mechanize
import urllib2
import re
import json

class DropboxConnection:
    """ Creates a connection to Dropbox """
    email = ""
    password = ""
    root_ns = ""
    token = ""
    browser = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login()
        self.get_constants()

    def login(self):
        """ Login to Dropbox and return mechanize browser instance """
        # Fire up a browser using mechanize
        self.browser = None  # mechanize.Browser()
        self.browser.set_handle_robots(False)
        # Browse to the login page
        self.browser.open('https://www.dropbox.com/login')
        # Enter the username and password into the login form
        isLoginForm = lambda l: l.action == "https://www.dropbox.com/login" and l.method == "POST"
        try:
            self.browser.select_form(predicate = isLoginForm)
        except:
            self.browser = None
            raise(Exception('Unable to find login form'))
        self.browser['login_email'] = self.email
        self.browser['login_password'] = self.password
        # Send the form
        _response = self.browser.submit()


    def get_constants(self):
        """ Load constants from page """
        home_src = self.browser.open('https://www.dropbox.com/home').read()
        try:
            self.root_ns = re.findall(r"root_ns: (\d+)", home_src)[0]
            self.token = re.findall(r"TOKEN: '(.+)'", home_src)[0]
        except:
            raise(Exception("Unable to find constants for AJAX requests"))

    def upload_file(self, local_file, remote_dir, remote_file):
        """ Upload a local file to Dropbox """
        if(not self.is_logged_in()):
            raise(Exception("Can't upload when not logged in"))
        self.browser.open('https://www.dropbox.com/')
        # Add our file upload to the upload form
        isUploadForm = lambda u: u.action == "https://dl-web.dropbox.com/upload" and u.method == "POST"
        try:
            self.browser.select_form(predicate = isUploadForm)
        except:
            raise(Exception('Unable to find upload form'))
        self.browser.form.find_control("dest").readonly = False
        self.browser.form.set_value(remote_dir, "dest")
        self.browser.form.add_file(open(local_file, "rb"), "", remote_file)
        # Submit the form with the file
        self.browser.submit()

    def get_dir_list(self, remote_dir):
        """ Get file info for a directory """
        if(not self.is_logged_in()):
            raise(Exception("Can't download when not logged in"))
        req_vars = "ns_id=" + self.root_ns + "&referrer=&t=" + self.token
        req = urllib2.Request('https://www.dropbox.com/browse' + remote_dir, data = req_vars)
        req.add_header('Referer', 'https://www.dropbox.com/home' + remote_dir)
        dir_info = json.loads(self.browser.open(req).read())
        dir_list = {}
        for item in dir_info['file_info']:
            # Eliminate directories
            if(item[0] == False):
                # get local filename
                absolute_filename = item[3]
                local_filename = re.findall(r".*\/(.*)", absolute_filename)[0]
                # get file URL and add it to the dictionary
                file_url = item[8]
                dir_list[local_filename] = file_url
        return dir_list

    def get_download_url(self, remote_dir, remote_file):
        """
        Get the URL to download a file
        """
        return self.get_dir_list(remote_dir)[remote_file]

    def download_file(self, remote_dir, remote_file, local_file):
        """
        Download a file and save it locally
        """
        fh = open(local_file, "wb")
        fh.write(self.browser.open(self.get_download_url(remote_dir, remote_file)).read())
        fh.close()

    def is_logged_in(self):
        """
        Checks if a login has been established
        """
        if(self.browser):
            return True
        else:
            return False












#!/usr/bin/env python

#********************************* README **************************************

# 0) DESCRIPTION:

# On invocation, the script creates a snapshot of ORIG_DIR's contents and writes
# it to BACKUP_DIR into 1) a new subdirectory or 2) a .tar.bz2 archive.
# The time of snapshot creation is written into the
# subdirectorie's name / archive file name. An optional second location can
# be defined to which the snapshot will be written additionally.

# This script is useful to manually and quickly create snapshots of a multi-file
# project you're working on, enabling _rollbacks_ to an older version of your
# project's files. Furthermore, using the additional backup location on another
# physical storage, the script prevents _data loss_.

# 1) USAGE:

# Download and install Python 2.7.x: http://python.org/download/

# Put the script file into the directory containing the directory you want to
# back up, adjust settings (below) and then run the script (doubleclick on Win).

# The snapshot/backup of
#  ./ORIG_DIR/*
# will go to
#  ./BACKUP_DIR/BACKUP_PREFIX_timestring/*       (SIMPLE method, built-in)
# OR to the archive
#  ./BACKUP_DIR/BACKUP_PREFIX_timestring.tar.bz2 (BZ2 method, built-in)
# Of course, ORIG_DIR and BACKUP_DIR can be absolute paths, too. Then, the
# location of this script does not matter.


ORIG_DIR = "/home"  # e.g. "." or "/home/user/"
BACKUP_DIR = "/root/dropbox_uploader"  # e.g. "/home/user/backup"
BACKUP_PREFIX = ""  # e.g. "user_bck"

# choose backup method: 'SIMPLE' OR 'BZ2':
# METHOD = 'SIMPLE'  # copy directory tree; e.g. if you don't have many files..
METHOD = 'BZ2'  # builtin method; if you like compression,

# set ADDITIONAL_BACKUP_DIR to double-save backup (e.g. on another hard disk)
# (outcomment the next line if this is desired behavior)
# ADDITIONAL_BACKUP_DIR = ""   # e.g. "/tmp"
#*******************************************************************************

import os
import time
import shutil
import sys
import tarfile
# import subprocess
import traceback
# from getpass import getpass

def exit_stop(p_msg):
    """DBK - this was missing
    """
    pass

def backup_directory_simple(srcdir, dstdir):

    if os.path.exists(dstdir):
        exit_stop("backup path %s already exists!" % dstdir)
    try:
        shutil.copytree(srcdir, dstdir)
    except:
        print "Error while copying tree in %s to %s" % (srcdir, dstdir)
        print "Traceback:\n%s" % traceback.format_exc()
        return False
    return dstdir

def backup_directory_bz2(srcdir, tarpath):
    if os.path.exists(tarpath):
        exit_stop("backup path %s already exists!" % tarpath)
    try:
        tar = tarfile.open(tarpath, "w:bz2")
        for filedir in os.listdir(srcdir):
            tar.add(os.path.join(srcdir, filedir), arcname = filedir)
        tar.close()
    except:
        print "Error while creating tar archive: %s" % tarpath
        print "Traceback:\n%s" % traceback.format_exc()
        return False
    return tarpath

def so_flushwr(string):
    sys.stdout.write(string)
    sys.stdout.flush()

# build timestring, check settings and invoke corresponding backup function
print ""
print "*********************************************************************"
print "* DropBox Backup script v.0.1a (very early alpha)                   *"
print "*                                                   created by c0da *"
print "*                                                    SEPTEMBER 2012 *"
print "*********************************************************************\n"

timestr = time.strftime("%d.%m.%Y-%H:%M:%S", time.localtime())

if METHOD not in ["SIMPLE", "BZ2"]:
    exit_stop("METHOD not 'SIMPLE' OR 'BZ2'")
if not os.path.exists(ORIG_DIR):
    exit_stop("ORIG_DIR does not exist: %s" % os.path.abspath(ORIG_DIR))
if not os.path.exists(BACKUP_DIR):
    exit_stop("BACKUP_DIR does not exist: %s" % os.path.abspath(BACKUP_DIR))
else:
    print ("Writing snapshot of\n    %s\n to\n    %s\nusing the %s method...\n" %
            (os.path.abspath(ORIG_DIR), os.path.abspath(BACKUP_DIR), METHOD))
    if METHOD == "SIMPLE":
        rv = backup_directory_simple(srcdir = ORIG_DIR,
            dstdir = os.path.join(BACKUP_DIR, BACKUP_PREFIX + timestr))
    elif METHOD == "BZ2":
        rv = backup_directory_bz2(srcdir = ORIG_DIR,
            tarpath = os.path.join(BACKUP_DIR,
                BACKUP_PREFIX + timestr + ".tar.bz2"))

if rv:
    print "Snapshot successfully written to\n  %s\n" % os.path.abspath(rv)
else:
    print "Failure during backup :-("
head, tail = os.path.split(os.path.abspath(rv))

try:
    conn = DropboxConnection("dropbox.email", "dropbox.password")
    conn.upload_file(tail, "/backup", tail)
except:
    print ("*********************************************************************")
    print ("* Upload failed. Try again!                                         *")
    print ("*********************************************************************")
else:
    os.remove(tail)
    print ("* Succes! File uploaded to your Dropbox                             *")
    print ("*********************************************************************")
sys.exit


















"""
#Default configuration file
CONFIG_FILE=~/.dropbox_uploader

#Default configuration file
CONFIG_FILE=~/.dropbox_uploader

#Default chunk size in Mb for the upload process
#It is recommended to increase this value only if you have enough free space on your /tmp partition
#Lower values may increase the number of http requests
CHUNK_SIZE=4

#Curl location
#If not set, curl will be searched into the $PATH
#CURL_BIN="/usr/bin/curl"

#Default values
TMP_DIR="/tmp"
DEBUG=0
QUIET=0
SHOW_PROGRESSBAR=0
SKIP_EXISTING_FILES=0
ERROR_STATUS=0


#Returns unix timestamp
function utime {
    echo $(date +%s)
}

#Remove temporary files
function remove_temp_files {
    if [[ $DEBUG == 0 ]]; then
        rm -fr "$RESPONSE_FILE"
        rm -fr "$CHUNK_FILE"
    fi
}

#Returns the file size in bytes
# generic GNU Linux: linux-gnu
# windows cygwin:    cygwin
# raspberry pi:      linux-gnueabihf
# macosx:            darwin10.0
# freebsd:           FreeBSD
# qnap:              linux-gnueabi
# iOS:               darwin9
function file_size {
    #Some embedded linux devices
    if [[ $OSTYPE == "linux-gnueabi" || $OSTYPE == "linux-gnu" ]]; then
        stat -c "%s" "$1"
        return

    #Generic Unix
    elif [[ ${OSTYPE:0:5} == "linux" || $OSTYPE == "cygwin" || ${OSTYPE:0:7} == "solaris" ]]; then
        stat --format="%s" "$1"
        return

    #BSD, OSX and other OSs
    else
        stat -f "%z" "$1"
        return
    fi
}

#Usage
function usage
{
    echo -e "Dropbox Uploader v$VERSION"
    echo -e "Andrea Fabrizi - andrea.fabrizi@gmail.com\n"
    echo -e "Usage: $0 COMMAND [PARAMETERS]..."
    echo -e "\nCommands:"

    echo -e "\t upload   <LOCAL_FILE/DIR ...>  <REMOTE_FILE/DIR>"
    echo -e "\t download <REMOTE_FILE/DIR> [LOCAL_FILE/DIR]"
    echo -e "\t delete   <REMOTE_FILE/DIR>"
    echo -e "\t move     <REMOTE_FILE/DIR> <REMOTE_FILE/DIR>"
    echo -e "\t copy     <REMOTE_FILE/DIR> <REMOTE_FILE/DIR>"
    echo -e "\t mkdir    <REMOTE_DIR>"
    echo -e "\t list     [REMOTE_DIR]"
    echo -e "\t share    <REMOTE_FILE>"
    echo -e "\t info"
    echo -e "\t unlink"

    echo -e "\nOptional parameters:"
    echo -e "\t-f <FILENAME> Load the configuration file from a specific file"
    echo -e "\t-s            Skip already existing files when download/upload. Default: Overwrite"
    echo -e "\t-d            Enable DEBUG mode"
    echo -e "\t-q            Quiet mode. Don't show messages"
    echo -e "\t-p            Show cURL progress meter"
    echo -e "\t-k            Doesn't check for SSL certificates (insecure)"

    echo -en "\nFor more info and examples, please see the README file.\n\n"
    remove_temp_files
    exit 1
}

#Check the curl exit code
function check_http_response
{
    CODE=$?

    #Checking curl exit code
    case $CODE in

        #OK
        0)

        ;;

        #Proxy error
        5)
            print "\nError: Couldn't resolve proxy. The given proxy host could not be resolved.\n"

            remove_temp_files
            exit 1
        ;;

        #Missing CA certificates
        60|58)
            print "\nError: cURL is not able to performs peer SSL certificate verification.\n"
            print "Please, install the default ca-certificates bundle.\n"
            print "To do this in a Debian/Ubuntu based system, try:\n"
            print "  sudo apt-get install ca-certificates\n\n"
            print "If the problem persists, try to use the -k option (insecure).\n"

            remove_temp_files
            exit 1
        ;;

        6)
            print "\nError: Couldn't resolve host.\n"

            remove_temp_files
            exit 1
        ;;

        7)
            print "\nError: Couldn't connect to host.\n"

            remove_temp_files
            exit 1
        ;;

    esac

    #Checking response file for generic errors
    if grep -q "HTTP/1.1 400" "$RESPONSE_FILE"; then
        ERROR_MSG=$(sed -n -e 's/{"error": "\([^"]*\)"}/\1/p' "$RESPONSE_FILE")

        case $ERROR_MSG in
             *access?attempt?failed?because?this?app?is?not?configured?to?have*)
                echo -e "\nError: The Permission type/Access level configured doesn't match the DropBox App settings!\nPlease run \"$0 unlink\" and try again."
                exit 1
            ;;
        esac

    fi

}

#Urlencode
function urlencode
{
    local string="${1}"
    local strlen=${#string}
    local encoded=""

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done

    echo "$encoded"
}

function normalize_path
{
    path=$(echo -e "$1")
    if [[ $HAVE_READLINK == 1 ]]; then
        readlink -m "$path"
    else
        echo "$path"
    fi
}

#Check if it's a file or directory
#Returns FILE/DIR/ERR
function db_stat
{
    local FILE=$(normalize_path "$1")

    #Checking if it's a file or a directory
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" "$API_METADATA_URL/$ACCESS_LEVEL/$(urlencode "$FILE")?oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" 2> /dev/null
    check_http_response

    #Even if the file/dir has been deleted from DropBox we receive a 200 OK response
    #So we must check if the file exists or if it has been deleted
    if grep -q "\"is_deleted\":" "$RESPONSE_FILE"; then
        local IS_DELETED=$(sed -n 's/.*"is_deleted":.\([^,]*\).*/\1/p' "$RESPONSE_FILE")
    else
        local IS_DELETED="false"
    fi

    #Exits...
    grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"
    if [[ $? == 0 && $IS_DELETED != "true" ]]; then

        local IS_DIR=$(sed -n 's/^\(.*\)\"contents":.\[.*/\1/p' "$RESPONSE_FILE")

        #It's a directory
        if [[ $IS_DIR != "" ]]; then
            echo "DIR"
        #It's a file
        else
            echo "FILE"
        fi

    #Doesn't exists
    else
        echo "ERR"
    fi
}

#Generic upload wrapper around db_upload_file and db_upload_dir functions
#$1 = Local source file/dir
#$2 = Remote destination file/dir
function db_upload
{
    local SRC=$(normalize_path "$1")
    local DST=$(normalize_path "$2")

    #Checking if the file/dir exists
    if [[ ! -e $SRC && ! -d $SRC ]]; then
        print " > No such file or directory: $SRC\n"
        ERROR_STATUS=1
        return
    fi

    #Checking if the file/dir has read permissions
    if [[ ! -r $SRC ]]; then
        print " > Error reading file $SRC: permission denied\n"
        ERROR_STATUS=1
        return
    fi

    #Checking if DST it's a folder or if it doesn' exists (in this case will be the destination name)
    TYPE=$(db_stat "$DST")
    if [[ $TYPE == "DIR" ]]; then
        local filename=$(basename "$SRC")
        DST="$DST/$filename"
    fi

    #It's a directory
    if [[ -d $SRC ]]; then
        db_upload_dir "$SRC" "$DST"

    #It's a file
    elif [[ -e $SRC ]]; then
        db_upload_file "$SRC" "$DST"

    #Unsupported object...
    else
        print " > Skipping not regular file \"$SRC\"\n"
    fi
}

#Generic upload wrapper around db_chunked_upload_file and db_simple_upload_file
#The final upload function will be choosen based on the file size
#$1 = Local source file
#$2 = Remote destination file
function db_upload_file
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    shopt -s nocasematch

    #Checking not allowed file names
    basefile_dst=$(basename "$FILE_DST")
    if [[ $basefile_dst == "thumbs.db" || \
          $basefile_dst == "desktop.ini" || \
          $basefile_dst == ".ds_store" || \
          $basefile_dst == "icon\r" || \
          $basefile_dst == ".dropbox" || \
          $basefile_dst == ".dropbox.attr" \
       ]]; then
        print " > Skipping not allowed file name \"$FILE_DST\"\n"
        return
    fi

    shopt -u nocasematch

    #Checking file size
    FILE_SIZE=$(file_size "$FILE_SRC")

    #Checking if the file already exists
    TYPE=$(db_stat "$FILE_DST")
    if [[ $TYPE != "ERR" && $SKIP_EXISTING_FILES == 1 ]]; then
        print " > Skipping already existing file \"$FILE_DST\"\n"
        return
    fi

    if [[ $FILE_SIZE -gt 157286000 ]]; then
        #If the file is greater than 150Mb, the chunked_upload API will be used
        db_chunked_upload_file "$FILE_SRC" "$FILE_DST"
    else
        db_simple_upload_file "$FILE_SRC" "$FILE_DST"
    fi

}

#Simple file upload
#$1 = Local source file
#$2 = Remote destination file
function db_simple_upload_file
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    if [[ $SHOW_PROGRESSBAR == 1 && $QUIET == 0 ]]; then
        CURL_PARAMETERS="--progress-bar"
        LINE_CR="\n"
    else
        CURL_PARAMETERS="-s"
        LINE_CR=""
    fi

    print " > Uploading \"$FILE_SRC\" to \"$FILE_DST\"... $LINE_CR"
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES $CURL_PARAMETERS -i --globoff -o "$RESPONSE_FILE" --upload-file "$FILE_SRC" "$API_UPLOAD_URL/$ACCESS_LEVEL/$(urlencode "$FILE_DST")?oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM"
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    else
        print "FAILED\n"
        print "An error occurred requesting /upload\n"
        ERROR_STATUS=1
    fi
}

#Chunked file upload
#$1 = Local source file
#$2 = Remote destination file
function db_chunked_upload_file
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    print " > Uploading \"$FILE_SRC\" to \"$FILE_DST\""

    local FILE_SIZE=$(file_size "$FILE_SRC")
    local OFFSET=0
    local UPLOAD_ID=""
    local UPLOAD_ERROR=0
    local CHUNK_PARAMS=""

    #Uploading chunks...
    while ([[ $OFFSET != $FILE_SIZE ]]); do

        let OFFSET_MB=$OFFSET/1024/1024

        #Create the chunk
        dd if="$FILE_SRC" of="$CHUNK_FILE" bs=1048576 skip=$OFFSET_MB count=$CHUNK_SIZE 2> /dev/null

        #Only for the first request these parameters are not included
        if [[ $OFFSET != 0 ]]; then
            CHUNK_PARAMS="upload_id=$UPLOAD_ID&offset=$OFFSET"
        fi

        #Uploading the chunk...
        $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --upload-file "$CHUNK_FILE" "$API_CHUNKED_UPLOAD_URL?$CHUNK_PARAMS&oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" 2> /dev/null
        check_http_response

        #Check
        if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
            print "."
            UPLOAD_ERROR=0
            UPLOAD_ID=$(sed -n 's/.*"upload_id": *"*\([^"]*\)"*.*/\1/p' "$RESPONSE_FILE")
            OFFSET=$(sed -n 's/.*"offset": *\([^}]*\).*/\1/p' "$RESPONSE_FILE")
        else
            print "*"
            let UPLOAD_ERROR=$UPLOAD_ERROR+1

            #On error, the upload is retried for max 3 times
            if [[ $UPLOAD_ERROR -gt 2 ]]; then
                print " FAILED\n"
                print "An error occurred requesting /chunked_upload\n"
                ERROR_STATUS=1
                return
            fi
        fi

    done

    UPLOAD_ERROR=0

    #Commit the upload
    while (true); do

        $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "upload_id=$UPLOAD_ID&oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" "$API_CHUNKED_UPLOAD_COMMIT_URL/$ACCESS_LEVEL/$(urlencode "$FILE_DST")" 2> /dev/null
        check_http_response

        #Check
        if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
            print "."
            UPLOAD_ERROR=0
            break
        else
            print "*"
            let UPLOAD_ERROR=$UPLOAD_ERROR+1

            #On error, the commit is retried for max 3 times
            if [[ $UPLOAD_ERROR -gt 2 ]]; then
                print " FAILED\n"
                print "An error occurred requesting /commit_chunked_upload\n"
                ERROR_STATUS=1
                return
            fi
        fi

    done

    print " DONE\n"
}

#Directory upload
#$1 = Local source dir
#$2 = Remote destination dir
function db_upload_dir
{
    local DIR_SRC=$(normalize_path "$1")
    local DIR_DST=$(normalize_path "$2")

    #Creatig remote directory
    db_mkdir "$DIR_DST"

    for file in "$DIR_SRC/"*; do
        db_upload "$file" "$DIR_DST"
    done
}

#Returns the free space on DropBox in bytes
function db_free_quota
{
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" "$API_INFO_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then

        quota=$(sed -n 's/.*"quota": \([0-9]*\).*/\1/p' "$RESPONSE_FILE")
        used=$(sed -n 's/.*"normal": \([0-9]*\).*/\1/p' "$RESPONSE_FILE")
        let free_quota=$quota-$used
        echo $free_quota

    else
        echo 0
    fi
}

#Generic download wrapper
#$1 = Remote source file/dir
#$2 = Local destination file/dir
function db_download
{
    local SRC=$(normalize_path "$1")
    local DST=$(normalize_path "$2")

    TYPE=$(db_stat "$SRC")

    #It's a directory
    if [[ $TYPE == "DIR" ]]; then

        #If the DST folder is not specified, I assume that is the current directory
        if [[ $DST == "" ]]; then
            DST="."
        fi

        #Checking if the destination directory exists
        if [[ ! -d $DST ]]; then
            local basedir=""
        else
            local basedir=$(basename "$SRC")
        fi

        local DEST_DIR=$(normalize_path "$DST/$basedir")
        print " > Downloading \"$SRC\" to \"$DEST_DIR\"... \n"
        print " > Creating local directory \"$DEST_DIR\"... "
        mkdir -p "$DEST_DIR"

        #Check
        if [[ $? == 0 ]]; then
            print "DONE\n"
        else
            print "FAILED\n"
            ERROR_STATUS=1
            return
        fi

        #Extracting directory content [...]
        #and replacing "}, {" with "}\n{"
        #I don't like this piece of code... but seems to be the only way to do this with SED, writing a portable code...
        local DIR_CONTENT=$(sed -n 's/.*: \[{\(.*\)/\1/p' "$RESPONSE_FILE" | sed 's/}, *{/}\
{/g')

        #Extracting files and subfolders
        TMP_DIR_CONTENT_FILE="${RESPONSE_FILE}_$RANDOM"
        echo "$DIR_CONTENT" | sed -n 's/.*"path": *"\([^"]*\)",.*"is_dir": *\([^"]*\),.*/\1:\2/p' > $TMP_DIR_CONTENT_FILE

        #For each entry...
        while read -r line; do

            local FILE=${line%:*}
            local TYPE=${line#*:}

            #Removing unneeded /
            FILE=${FILE##*/}

            if [[ $TYPE == "false" ]]; then
                db_download_file "$SRC/$FILE" "$DEST_DIR/$FILE"
            else
                db_download "$SRC/$FILE" "$DEST_DIR"
            fi

        done < $TMP_DIR_CONTENT_FILE

        rm -fr $TMP_DIR_CONTENT_FILE

    #It's a file
    elif [[ $TYPE == "FILE" ]]; then

        #Checking DST
        if [[ $DST == "" ]]; then
            DST=$(basename "$SRC")
        fi

        #If the destination is a directory, the file will be download into
        if [[ -d $DST ]]; then
            DST="$DST/$SRC"
        fi

        db_download_file "$SRC" "$DST"

    #Doesn't exists
    else
        print " > No such file or directory: $SRC\n"
        ERROR_STATUS=1
        return
    fi
}

#Simple file download
#$1 = Remote source file
#$2 = Local destination file
function db_download_file
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    if [[ $SHOW_PROGRESSBAR == 1 && $QUIET == 0 ]]; then
        CURL_PARAMETERS="--progress-bar"
        LINE_CR="\n"
    else
        CURL_PARAMETERS="-s"
        LINE_CR=""
    fi

    #Checking if the file already exists
    if [[ -e $FILE_DST && $SKIP_EXISTING_FILES == 1 ]]; then
        print " > Skipping already existing file \"$FILE_DST\"\n"
        return
    fi

    #Creating the empty file, that for two reasons:
    #1) In this way I can check if the destination file is writable or not
    #2) Curl doesn't automatically creates files with 0 bytes size
    dd if=/dev/zero of="$FILE_DST" count=0 2> /dev/null
    if [[ $? != 0 ]]; then
        print " > Error writing file $FILE_DST: permission denied\n"
        ERROR_STATUS=1
        return
    fi

    print " > Downloading \"$FILE_SRC\" to \"$FILE_DST\"... $LINE_CR"
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES $CURL_PARAMETERS --globoff -D "$RESPONSE_FILE" -o "$FILE_DST" "$API_DOWNLOAD_URL/$ACCESS_LEVEL/$(urlencode "$FILE_SRC")?oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM"
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    else
        print "FAILED\n"
        rm -fr "$FILE_DST"
        ERROR_STATUS=1
        return
    fi
}

#Prints account info
function db_account_info
{
    print "Dropbox Uploader v$VERSION\n\n"
    print " > Getting info... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" "$API_INFO_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then

        name=$(sed -n 's/.*"display_name": "\([^"]*\).*/\1/p' "$RESPONSE_FILE")
        echo -e "\n\nName:\t$name"

        uid=$(sed -n 's/.*"uid": \([0-9]*\).*/\1/p' "$RESPONSE_FILE")
        echo -e "UID:\t$uid"

        email=$(sed -n 's/.*"email": "\([^"]*\).*/\1/p' "$RESPONSE_FILE")
        echo -e "Email:\t$email"

        quota=$(sed -n 's/.*"quota": \([0-9]*\).*/\1/p' "$RESPONSE_FILE")
        let quota_mb=$quota/1024/1024
        echo -e "Quota:\t$quota_mb Mb"

        used=$(sed -n 's/.*"normal": \([0-9]*\).*/\1/p' "$RESPONSE_FILE")
        let used_mb=$used/1024/1024
        echo -e "Used:\t$used_mb Mb"

        let free_mb=($quota-$used)/1024/1024
        echo -e "Free:\t$free_mb Mb"

        echo ""

    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#Account unlink
function db_unlink
{
    echo -ne "Are you sure you want unlink this script from your Dropbox account? [y/n]"
    read answer
    if [[ $answer == "y" ]]; then
        rm -fr "$CONFIG_FILE"
        echo -ne "DONE\n"
    fi
}

#Delete a remote file
#$1 = Remote file to delete
function db_delete
{
    local FILE_DST=$(normalize_path "$1")

    print " > Deleting \"$FILE_DST\"... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM&root=$ACCESS_LEVEL&path=$(urlencode "$FILE_DST")" "$API_DELETE_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#Move/Rename a remote file
#$1 = Remote file to rename or move
#$2 = New file name or location
function db_move
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    TYPE=$(db_stat "$FILE_DST")

    #If the destination it's a directory, the source will be moved into it
    if [[ $TYPE == "DIR" ]]; then
        local filename=$(basename "$FILE_SRC")
        FILE_DST=$(normalize_path "$FILE_DST/$filename")
    fi

    print " > Moving \"$FILE_SRC\" to \"$FILE_DST\" ... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM&root=$ACCESS_LEVEL&from_path=$(urlencode "$FILE_SRC")&to_path=$(urlencode "$FILE_DST")" "$API_MOVE_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#Copy a remote file to a remote location
#$1 = Remote file to rename or move
#$2 = New file name or location
function db_copy
{
    local FILE_SRC=$(normalize_path "$1")
    local FILE_DST=$(normalize_path "$2")

    TYPE=$(db_stat "$FILE_DST")

    #If the destination it's a directory, the source will be copied into it
    if [[ $TYPE == "DIR" ]]; then
        local filename=$(basename "$FILE_SRC")
        FILE_DST=$(normalize_path "$FILE_DST/$filename")
    fi

    print " > Copying \"$FILE_SRC\" to \"$FILE_DST\" ... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM&root=$ACCESS_LEVEL&from_path=$(urlencode "$FILE_SRC")&to_path=$(urlencode "$FILE_DST")" "$API_COPY_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#Create a new directory
#$1 = Remote directory to create
function db_mkdir
{
    local DIR_DST=$(normalize_path "$1")

    print " > Creating Directory \"$DIR_DST\"... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM&root=$ACCESS_LEVEL&path=$(urlencode "$DIR_DST")" "$API_MKDIR_URL" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print "DONE\n"
    elif grep -q "^HTTP/1.1 403 Forbidden" "$RESPONSE_FILE"; then
        print "ALREADY EXISTS\n"
    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#List remote directory
#$1 = Remote directory
function db_list
{
    local DIR_DST=$(normalize_path "$1")

    print " > Listing \"$DIR_DST\"... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" "$API_METADATA_URL/$ACCESS_LEVEL/$(urlencode "$DIR_DST")?oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then

        local IS_DIR=$(sed -n 's/^\(.*\)\"contents":.\[.*/\1/p' "$RESPONSE_FILE")

        #It's a directory
        if [[ $IS_DIR != "" ]]; then

            print "DONE\n"

            #Extracting directory content [...]
            #and replacing "}, {" with "}\n{"
            #I don't like this piece of code... but seems to be the only way to do this with SED, writing a portable code...
            local DIR_CONTENT=$(sed -n 's/.*: \[{\(.*\)/\1/p' "$RESPONSE_FILE" | sed 's/}, *{/}\
{/g')

            #Converting escaped quotes to unicode format and extracting files and subfolders
            echo "$DIR_CONTENT" | sed 's/\\"/\\u0022/' | sed -n 's/.*"bytes": *\([0-9]*\),.*"path": *"\([^"]*\)",.*"is_dir": *\([^"]*\),.*/\2:\3;\1/p' > $RESPONSE_FILE

            #Looking for the biggest file size
            #to calculate the padding to use
            local padding=0
            while read -r line; do
                local FILE=${line%:*}
                local META=${line##*:}
                local SIZE=${META#*;}

                if [[ ${#SIZE} -gt $padding ]]; then
                    padding=${#SIZE}
                fi
            done < $RESPONSE_FILE

            #For each entry...
            while read -r line; do

                local FILE=${line%:*}
                local META=${line##*:}
                local TYPE=${META%;*}
                local SIZE=${META#*;}

                #Removing unneeded /
                FILE=${FILE##*/}

                if [[ $TYPE == "false" ]]; then
                    TYPE="F"
                else
                    TYPE="D"
                fi

                FILE=$(echo -e "$FILE")
                printf " [$TYPE] %-${padding}s %s\n" "$SIZE" "$FILE"

            done < $RESPONSE_FILE

        #It's a file
        else
            print "FAILED: $DIR_DST is not a directory!\n"
            ERROR_STATUS=1
        fi

    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

#Share remote file
#$1 = Remote file
function db_share
{
    local FILE_DST=$(normalize_path "$1")

    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o "$RESPONSE_FILE" "$API_SHARES_URL/$ACCESS_LEVEL/$(urlencode "$FILE_DST")?oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_ACCESS_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_ACCESS_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM&short_url=false" 2> /dev/null
    check_http_response

    #Check
    if grep -q "^HTTP/1.1 200 OK" "$RESPONSE_FILE"; then
        print " > Share link: "
        echo $(sed -n 's/.*"url": "\([^"]*\).*/\1/p' "$RESPONSE_FILE")
    else
        print "FAILED\n"
        ERROR_STATUS=1
    fi
}

################
#### SETUP  ####
################

#CHECKING FOR AUTH FILE
if [[ -e $CONFIG_FILE ]]; then

    #Loading data... and change old format config if necesary.
    source "$CONFIG_FILE" 2>/dev/null || {
        sed -i'' 's/:/=/' "$CONFIG_FILE" && source "$CONFIG_FILE" 2>/dev/null
    }

    #Checking the loaded data
    if [[ $APPKEY == "" || $APPSECRET == "" || $OAUTH_ACCESS_TOKEN_SECRET == "" || $OAUTH_ACCESS_TOKEN == "" ]]; then
        echo -ne "Error loading data from $CONFIG_FILE...\n"
        echo -ne "It is recommended to run $0 unlink\n"
        remove_temp_files
        exit 1
    fi

    #Back compatibility with previous Dropbox Uploader versions
    if [[ $ACCESS_LEVEL == "" ]]; then
        ACCESS_LEVEL="dropbox"
    fi

#NEW SETUP...
else

    echo -ne "\n This is the first time you run this script.\n\n"
    echo -ne " 1) Open the following URL in your Browser, and log in using your account: $APP_CREATE_URL\n"
    echo -ne " 2) Click on \"Create App\", then select \"Dropbox API app\"\n"
    echo -ne " 3) Select \"Files and datastores\"\n"
    echo -ne " 4) Now go on with the configuration, choosing the app permissions and access restrictions to your DropBox folder\n"
    echo -ne " 5) Enter the \"App Name\" that you prefer (e.g. MyUploader$RANDOM$RANDOM$RANDOM)\n\n"

    echo -ne " Now, click on the \"Create App\" button.\n\n"

    echo -ne " When your new App is successfully created, please type the\n"
    echo -ne " App Key, App Secret and the Permission type shown in the confirmation page:\n\n"

    #Getting the app key and secret from the user
    while (true); do

        echo -n " # App key: "
        read APPKEY

        echo -n " # App secret: "
        read APPSECRET

        echo -n " # Permission type, App folder or Full Dropbox [a/f]: "
        read ACCESS_LEVEL

        if [[ $ACCESS_LEVEL == "a" ]]; then
            ACCESS_LEVEL="sandbox"
            ACCESS_MSG="App Folder"
        else
            ACCESS_LEVEL="dropbox"
            ACCESS_MSG="Full Dropbox"
        fi

        echo -ne "\n > App key is $APPKEY, App secret is $APPSECRET and Access level is $ACCESS_MSG. Looks ok? [y/n]"
        read answer
        if [[ $answer == "y" ]]; then
            break;
        fi

    done

    #TOKEN REQUESTS
    echo -ne "\n > Token request... "
    $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o $RESPONSE_FILE --data "oauth_consumer_key=$APPKEY&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" "$API_REQUEST_TOKEN_URL" 2> /dev/null
    check_http_response
    OAUTH_TOKEN_SECRET=$(sed -n 's/oauth_token_secret=\([a-z A-Z 0-9]*\).*/\1/p' "$RESPONSE_FILE")
    OAUTH_TOKEN=$(sed -n 's/.*oauth_token=\([a-z A-Z 0-9]*\)/\1/p' "$RESPONSE_FILE")

    if [[ $OAUTH_TOKEN != "" && $OAUTH_TOKEN_SECRET != "" ]]; then
        echo -ne "OK\n"
    else
        echo -ne " FAILED\n\n Please, check your App key and secret...\n\n"
        remove_temp_files
        exit 1
    fi

    while (true); do

        #USER AUTH
        echo -ne "\n Please open the following URL in your browser, and allow Dropbox Uploader\n"
        echo -ne " to access your DropBox folder:\n\n --> ${API_USER_AUTH_URL}?oauth_token=$OAUTH_TOKEN\n"
        echo -ne "\nPress enter when done...\n"
        read

        #API_ACCESS_TOKEN_URL
        echo -ne " > Access Token request... "
        $CURL_BIN $CURL_ACCEPT_CERTIFICATES -s --show-error --globoff -i -o $RESPONSE_FILE --data "oauth_consumer_key=$APPKEY&oauth_token=$OAUTH_TOKEN&oauth_signature_method=PLAINTEXT&oauth_signature=$APPSECRET%26$OAUTH_TOKEN_SECRET&oauth_timestamp=$(utime)&oauth_nonce=$RANDOM" "$API_ACCESS_TOKEN_URL" 2> /dev/null
        check_http_response
        OAUTH_ACCESS_TOKEN_SECRET=$(sed -n 's/oauth_token_secret=\([a-z A-Z 0-9]*\)&.*/\1/p' "$RESPONSE_FILE")
        OAUTH_ACCESS_TOKEN=$(sed -n 's/.*oauth_token=\([a-z A-Z 0-9]*\)&.*/\1/p' "$RESPONSE_FILE")
        OAUTH_ACCESS_UID=$(sed -n 's/.*uid=\([0-9]*\)/\1/p' "$RESPONSE_FILE")

        if [[ $OAUTH_ACCESS_TOKEN != "" && $OAUTH_ACCESS_TOKEN_SECRET != "" && $OAUTH_ACCESS_UID != "" ]]; then
            echo -ne "OK\n"

            #Saving data in new format, compatible with source command.
            echo "APPKEY=$APPKEY" > "$CONFIG_FILE"
            echo "APPSECRET=$APPSECRET" >> "$CONFIG_FILE"
            echo "ACCESS_LEVEL=$ACCESS_LEVEL" >> "$CONFIG_FILE"
            echo "OAUTH_ACCESS_TOKEN=$OAUTH_ACCESS_TOKEN" >> "$CONFIG_FILE"
            echo "OAUTH_ACCESS_TOKEN_SECRET=$OAUTH_ACCESS_TOKEN_SECRET" >> "$CONFIG_FILE"

            echo -ne "\n Setup completed!\n"
            break
        else
            print " FAILED\n"
            ERROR_STATUS=1
        fi

    done;

    remove_temp_files
    exit $ERROR_STATUS
fi

################
#### START  ####
################

COMMAND=${@:$OPTIND:1}
ARG1=${@:$OPTIND+1:1}
ARG2=${@:$OPTIND+2:1}

let argnum=$#-$OPTIND

#CHECKING PARAMS VALUES
case $COMMAND in

    upload)
        if [[ $argnum -lt 2 ]]; then
            usage
        fi
        FILE_DST=${@:$#:1}
        for (( i=$OPTIND+1; i<$#; i++ )); do
            FILE_SRC=${@:$i:1}
            db_upload "$FILE_SRC" "/$FILE_DST"
        done
    ;;

    download)
        if [[ $argnum -lt 1 ]]; then
            usage
        fi
        FILE_SRC=$ARG1
        FILE_DST=$ARG2
        db_download "/$FILE_SRC" "$FILE_DST"
    ;;

    share)
        if [[ $argnum -lt 1 ]]; then
            usage
        fi
        FILE_DST=$ARG1
        db_share "/$FILE_DST"
    ;;

    info)
        db_account_info
    ;;

    delete|remove)
        if [[ $argnum -lt 1 ]]; then
            usage
        fi
        FILE_DST=$ARG1
        db_delete "/$FILE_DST"
    ;;

    move|rename)
        if [[ $argnum -lt 2 ]]; then
            usage
        fi
        FILE_SRC=$ARG1
        FILE_DST=$ARG2
        db_move "/$FILE_SRC" "/$FILE_DST"
    ;;

    copy)
        if [[ $argnum -lt 2 ]]; then
            usage
        fi
        FILE_SRC=$ARG1
        FILE_DST=$ARG2
        db_copy "/$FILE_SRC" "/$FILE_DST"
    ;;

    mkdir)
        if [[ $argnum -lt 1 ]]; then
            usage
        fi
        DIR_DST=$ARG1
        db_mkdir "/$DIR_DST"
    ;;

    list)
        DIR_DST=$ARG1
        #Checking DIR_DST
        if [[ $DIR_DST == "" ]]; then
            DIR_DST="/"
        fi
        db_list "/$DIR_DST"
    ;;

    unlink)
        db_unlink
    ;;

esac

remove_temp_files
exit $ERROR_STATUS



"""
