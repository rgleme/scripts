#!/bin/sh
#Usage: Should be used on Crontab routines.Its made for NAT uplinks.
 
KEYDYN="v9BhsbwDu4q95g/Gf/EiXA=="
IFACE="eth2"
ISHORT="2"
ISPROG=is-dyndns-nat-$IFACE
HST=`hostname`
EMAIL=alert-link@n.inter.bz
DATE=`date +'%b %d %H:%M:%S'`
 
[ ! -d /var/log/is ] && mkdir /var/log/is
 
IPINT=`curl --interface $IFACE -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'`
 
if [ -z "$IPINT" ] ; then
    echo "$DATE $HST $ISPROG: Can't find EXTERNAL IP for $IFACE" >> /var/log/is/is-dyndns-nat.log
    exit 1
fi
 
IPDNS=`dig +short @a.inter.com.br ${HST}${ISHORT}.t.inter.bz`
 
if [ -z "$IPDNS" ] ; then
    ping -W 2 -I $IFACE -c 3 a.inter.com.br > /dev/null 2>&1
    RETPING1=$?
    if [ $RETPING1 -eq 0 ] ; then
        echo "$DATE $HST $ISPROG: INFO: Can't find DNS IP for ${HST}${ISHORT}.t.inter.bz" >> /var/log/is/is-dyndns-nat.log
    else
        VAR=`date -r /tmp/is-dyndns-nat-$IFACE.control +'%G%m%d%H%M%S'`
        AGO=`date +'%G%m%d%H%M%S' --date="6 hours ago"`
        echo "$DATE $HST $ISPROG: FAILURE: Can't connect to DNS server - Aborting..." >> /var/log/is/is-dyndns-nat.log
        if [ "$VAR" < "$AGO" ] || [ -z "$VAR" ]; then
            [ $EMAIL ] && mail -s "$HST $ISPROG: FAILURE: Can't connect to DNS server - Aborting..." $EMAIL <. >>/dev/null
            touch /tmp/is-dyndns-nat-$IFACE.control
            exit 1
        fi
    fi
fi
 
if [ "$IPINT" != "$IPDNS" ] ; then
    echo "update delete ${HST}${ISHORT}.t.inter.bz."  > /tmp/zonetest
    echo "update add ${HST}${ISHORT}.t.inter.bz. 60 IN A $IPINT" >> /tmp/zonetest
    echo "update add ${HST}${ISHORT}.t.inter.bz. 60 TXT \"Updated on $DATE\"" >> /tmp/zonetest
    echo "send" >> /tmp/zonetest
    nsupdate -y keydyn:$KEYDYN /tmp/zonetest
    RC=$?
    if [ $RC != 0 ]; then
        VAR=`date -r /tmp/is-dyndns-nat-$IFACE.control +'%G%m%d%H%M%S'`
        AGO=`date +'%G%m%d%H%M%S' --date="6 hours ago"`
        echo "$DATE $HST $ISPROG: FAILURE: Updating dynamic IP $IPINT for $IFACE failed (RC=$RC)" >> /var/log/is/is-dyndns-nat.log
        if [ "$VAR" < "$AGO" ] || [ -z "$VAR" ]; then
            [ $EMAIL ] && mail -s "$HST $ISPROG: FAILURE: Updating dynamic IP $IPINT for $IFACE failed" $EMAIL <. >>/dev/null
            touch /tmp/is-dyndns-nat-$IFACE.control
        fi
    else
        echo "$DATE $HST $ISPROG: SUCCESS: Updating dynamic IP $IPINT for $IFACE succeeded" >> /var/log/is/is-dyndns-nat.log
    fi
else
    echo "$DATE $HST $ISPROG: INFO: Nothing changed. Same IP: $IPINT for $IFACE" >> /var/log/is/is-dyndns-nat.log
    exit 0
fi
