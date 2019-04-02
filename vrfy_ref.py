#!/usr/bin/python

import socket
import sys


class Vrfy:

    def __init__(self):

        ip_input = input("Enter IP address: ")

        # create a socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server
        self.connect = self.s.connect((ip_input, 25))

        # receive the banner
        banner = self.s.recv(1024)

        print(banner)


        # VRFY a user
        self.s.send('VRFY ' + sys.argv[1] + '\r\n')
        results = self.s.recv(1024)
        print(results)
        self.s.close()


def main():
    Vrfy()


if __name__ == '__main__':
    main()
