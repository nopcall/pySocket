#!/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

from concurrent.futures import *

HOST = '127.0.0.1'
PORT = 1234

def say_hello(arg):
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    while True:
        time.sleep(random.randrange(1, 3))
        client_socket.send(str(client_socket.getsockname()[1]).encode())
        buf = client_socket.recv(1024)
        #print(buf.decode())

def main():
    executor = ThreadPoolExecutor(max_workers=2048)
    executor.map(say_hello, [i for i in range(0, 2048)])

if __name__ == '__main__':
    main()
