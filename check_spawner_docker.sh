#!/bin/bash

SERVICE="provis_container_hk_docker"

MONITOR="provis_container_hk_docker"

ITEM="provis_container_hk_docker"

SENDXML="/export/scripts/send-xml.pl"

validacao(){
CURL=$(curl -si -H 'X-Container-Engine: docker' -H "Host: provisconthk.eti.br" -H "X-User: provisconthk" -H "User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3"  -H "Accept: */*"  -H "X-User-Domains: provisconthk.eti.br"  -H "X-Homedir: a2-nagel-pool02/pool02-fs0007/a1/provisconthk/home"  -H "X-Application: http-server=httpd;template=php56"  -H "X-Instance: 1"  -H "X-Memory-Limit: 256"  -H "X-CPU-Limit: 25"  -H "X-Idle-Timeout: 1" -H "X-Backend: b:u:provisconthk:1" -H "X-Realhost:provisconthk.eti.br" http://loghost:80/)
}

send_quebec(){
$SENDXML -i "$ITEM" -m "$MONITOR" -v "$MSG" -s "$SERVICE" -u "$STATUS"  -a false
exit 0;
}



sed -n "/^$(date --date='30 minutes ago' '+%Y\/%m\/%d %H:%M')/,\$p" /export/logs/UOLHOST-supervisor/phoenix.log | grep -q spawned
return1=$?

if [ $return1 -eq 0 ]
        then

                MSG="ok"
                STATUS="0"
                send_quebec
        else

                validacao
                echo $CURL | grep 200
                return2=$?

                        if [ $return2 -eq 0 ]
                                then

                                        MSG="ok"
                                        STATUS="0"
                                        send_quebec
                                else
                
                                        MSG="Provisionamento de container inconsistente"
                                        STATUS="1"
                                        send_quebec
                                fi
fi
