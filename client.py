#!/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

HOST = '127.0.0.1'
PORT = 1234

def say_hello():
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    while True:
        time.sleep(random.randrange(1, 3))
        client_socket.send(str(client_socket.getsockname()[1]).encode())
        buf = client_socket.recv(1024)
        #print(buf.decode())

def main():
    threads = []
    for i in range(0, 2048):
        t = threading.Thread(target=say_hello)
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    input("waiting ...")

if __name__ == '__main__':
    main()
