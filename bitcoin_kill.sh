#!/bin/bash

logfile="/var/log/bitcoin.log"
dump="/tmp/dump.log"
date=$(date '+%d/%m/%Y %H:%M:%S')

ps axuf | grep -v root | grep '\-c /tmp\|cryptonight\|xm2sg|/var/tmp\|backupm\|annod\|annizod' > $dump

        while IFS='' read -r ps
                do
                        user=$(echo $ps | awk {'print $1'})
                        pid=$(echo $ps | awk {'print $2'})
                        echo "$date --- $user com processo de mineracao" >> $logfile
                        kill -9 $pid
                done < $dump
