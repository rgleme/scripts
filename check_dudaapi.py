#!/usr/bin/python

import telnetlib, subprocess

SERVICE="check_dudaapi"
MONITOR="check_dudaapi"
ITEM="check_dudaapi"
SENDXML="/export/scripts/send-xml.pl"



host = "api.dudamobile.com"
port = 443
timeout = 5


tn = telnetlib.Telnet(host,port,timeout)

def telnet():

        if  tn:
                status = {'msg': 'OK', 'status': '0'}
                return status

retorno=telnet()
MSG = retorno['msg']
STATUS = retorno['status']

subprocess.call([SENDXML, '-i', ITEM, '-m', MONITOR, '-v', MSG, '-s', SERVICE, '-u', STATUS, '-a', 'false'])
