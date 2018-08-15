#!/usr/bin/python

import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(user,reseller):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Report Mineracao de BitCoin | Usuario: %s'%user
	FROM = "abuse@%s"%socket.gethostname()
	TO = ["teste@uol.com.br","teste@uolinc.com"]
	msg['From'] = FROM
	msg['To'] = ', '.join(TO)
	text = "\n \
                Houve um bloqueio automatico no servidor %s onde foi encontrado um ou mais scripts de mineracao de BitCoin\n \
                Seguem os dados para notificacao:\n \
                Usuario: %s\n \
                Revendedor: %s\n \
                Favor notificar o cliente!\n \
                Duvidas, entrar em contato com teste@uolinc.com"%(socket.gethostname(),user,reseller)
	part1 = MIMEText(text, 'plain')
	msg.attach(part1)
	s = smtplib.SMTP('localhost')
	#s.set_debuglevel(3)
	s.sendmail(FROM, TO, msg.as_string())
	s.quit()
