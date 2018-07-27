#!/bin/bash

LOG_FILE=/var/log/whm_watch_log

if
        /sbin/iptables -I INPUT -s $1 -j DROP
                then echo "[`date`] IP $1 bloqueado no IPTABLES" >> $LOG_FILE
fi
