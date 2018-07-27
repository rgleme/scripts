#!/bin/bash

iptables="/sbin/iptables"
logfile="/var/log/dropflood.log"
dump="/tmp/dump.log"
lock_file="/tmp/listflood.lock"
max_con=40

if [[ -f $lock_file ]];
then
        echo "lockile existe"
        exit 1;
else

touch $lock_file
fi


    netstat -ant |grep :80 | egrep ESTABLISHED | awk '{print $5}' | egrep -v "200.221|200.98" | cut -d ':' -f 1 | sort | uniq -c | sort -n | awk '{print $1":"$2}' > $dump

        while IFS='' read -r con
                do
                        qtd=$( echo $con | cut -d ':' -f 1)
                        ip=$( echo $con | cut -d ':' -f 2)
                                if [[ $qtd -gt $max_con ]] ; then
                                        echo "$ip com $qtd conexoes" >> $logfile
                                        check_rule=$(iptables -nL | grep -c $ip)
                                                if [[ $check_rule -gt 0 ]] ;then
                                                        echo "regra existente para ip: $ip"
                                                else
                                                        $iptables -A INPUT -s $ip -j DROP
                                                        echo "$ip bloqueado" >> $logfile
                                                fi
                                fi
                done < $dump
                rm -f $lock_file
