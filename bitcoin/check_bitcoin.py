#! /usr/bin/python

import fnmatch
import os
import json
import subprocess

from Email.send_email import send

def seek():
	lista = []
	for root,dirs,files in os.walk("/home/"):
		for name in fnmatch.filter(files, "stylewpp.php*"):
			res = name
			if res:
				y = root.split("/")
				if y[2] not in lista:
					lista.append(y[2])
	return lista

def destroy(arg):
	for i in arg:
		subprocess.call(["/scripts/suspendacct",i])
		info = subprocess.check_output(["/sbin/whmapi1", "accountsummary", "-o", "json", "user="+i])
		user_dict = json.loads(info)
		arg2 = user_dict['data']['acct'][0]['owner']
		send(i,arg2)

if __name__ == '__main__':
	destroy(seek())
