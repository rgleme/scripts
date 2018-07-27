#!/bin/bash

LOG_FILE=/var/log/whm_watch_log

if
        /sbin/iptables -I INPUT -s $1 -j DROP
                then echo "[`date`] IP $1 bloqueado no IPTABLES" >> $LOG_FILE
fi
[root@a1-caju1 whm_block]# cat whm_watch.sh 
#!/bin/bash

## Script para bloquear o acesso ao WHM pelo usuario ROOT, de IPs nao autorizados

PID_FILE=/var/tmp/whm_watch.pid
WATCH_FILE=/usr/local/cpanel/logs/access_log
WHITE_LIST=/export/scripts/whm_block/whm_whitelist
IPTABLES_BLOCK=/export/scripts/whm_block/block_iptables.sh

for CUR_PID in `cat $PID_FILE 2> /dev/null`;
        do
                if grep $0 /proc/$CUR_PID/cmdline &> /dev/null
                        then
                                if [[ "$1" == "kill" ]]
                                        then
                                                pkill -TERM -P $CUR_PID
                                                exit 0
                                fi
                        echo "WHM Watch is already running... (PID $CUR_PID)"
                        exit 1
                fi
        done

echo "WHM Watch started (PID $$)"
echo $$ > $PID_FILE
tail -1f $WATCH_FILE | grep --line-buffered -E ' - root ' | grep --line-buffered -Po "^[0-9\.]*" | grep --line-buffered -vf $WHITE_LIST | xargs -r -i -n 1 $IPTABLES_BLOCK {}
