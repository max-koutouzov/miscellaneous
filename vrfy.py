#!/usr/bin/python

from time import sleep
import socket
import sys
import os


class Vrfy:

    @staticmethod
    def check_file():
        if os.path.isfile('users.txt'):
            print('Reading users.txt file')
        else:
            print("Create users.txt file in this directory")
            sys.exit(0)

    @staticmethod
    def connect():

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(('10.11.24.18', 25))

        banner = s.recv(1024)

        print(banner)

        with open('users.txt', 'r') as fi:

            for line in fi.readlines():
                s.send('VRFY ' + line + '\r\n')
                result = s.recv(1024)
                print(result)
                sleep(1)

                s.close()


def main():
    vrfy = Vrfy()
    vrfy.check_file()
    vrfy.connect()


if __name__ == '__main__':
    main()

