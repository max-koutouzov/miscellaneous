#!/usr/bin/python


import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print("\nSending evil buffer")
    s.connect(('10.11.24.18', 110))
    data = s.recv(1024)
    print(data)

    s.send('User guest' + '\r\n')
    data = s.recv(1024)
    print(data)

    s.send('PASS password\r\n')
    data = s.recv(1024)
    print(data)

    s.close()
    print('\nDone!')

except Exception as e:
    print(e, "Could not connect to POP3!")