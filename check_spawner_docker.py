#!/usr/bin/python

import requests, subprocess

SERVICE="provis_container_hk_docker"
MONITOR="provis_container_hk_docker"
ITEM="provis_container_hk_docker"
SENDXML="/export/scripts/send-xml.pl"

headers = {"X-Container-Engine": "docker",
           "Host": "provisconthk.eti.br",
           "X-User": "provisconthk",
           "User-Agent": "curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3",
           "Accept": "*/*",
           "X-Homedir": "a2-nagel-pool02/pool02-fs0007/a1/provisconthk/home",
           "X-Application": "http-server=httpd;template=php56",
           "X-Instance": "1",
           "X-Memory-Limit": "256",
           "X-CPU-Limit": "25",
           "X-Idle-Timeout": "1",
           "X-Backend": "b:u:provisconthk:1",
           "X-Realhost": "provisconthk.eti.br",
           }

def validacao ():
        try:
                a = subprocess.check_call(["docker events --since '120m' --until '0m' --filter 'event=create' --format Name={{.Actor.Attributes.name}} | grep -v provisconthk"], shell=True)
                if a == 0:
                        status = {'msg': 'OK', 'status': '0'}
                        return status
        except:
                r = requests.post("http://loghost", headers=headers)
                if r.status_code == 200:
                        status = {'msg': 'PROVISIONAMENTO OK, MAS NAO HA CLIENTES REAIS', 'status': '1'}
                        return status
                else:
                        status = {'msg': 'PROVISIONAMENTO COM FALHA', 'status': '1'}
                        return status

def send_quebec (status):
        MSG = status['msg']
        STATUS = status['status']
        subprocess.call([SENDXML, '-i', ITEM, '-m', MONITOR, '-v', MSG, '-s', SERVICE, '-u', STATUS, '-a', 'false'])

if __name__ == '__main__':
        send_quebec(validacao())
