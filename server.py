#!/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select
from multiprocessing.pool import ThreadPool

PORT = 1234
MAX_LISTEN = 64

clients = {}
messages = {}
responses = {}

def handle_connect(server_socket):
    # new client connected
    cfd, caddr = server_socket.accept()
    cfd.setblocking(False)
    server_epoll.register(cfd.fileno(), select.EPOLLIN)

    clients[cfd.fileno()] = cfd
    messages[cfd.fileno()] = b''
    responses[cfd.fileno()] = b''

def handle_diconnect(efd):
    # client disconnected
    server_epoll.unregister(efd)
    clients[efd].close()

    del messages[efd]
    del responses[efd]
    print("{fd}: disconnected".format(fd=efd))

def handle_in(efd):
    # got client message
    messages[efd] += clients[efd].recv(1024) # receiv 1024 bytes
    print("{fd}:".format(fd=efd), messages[efd].decode())
    messages[efd] = b''
    responses[efd] = b'Got Your Message'
    server_epoll.modify(efd, select.EPOLLOUT)

def handle_out(efd):
    # sent message to client
    sent_count = clients[efd].send(responses[efd])
    responses[efd] = responses[efd][sent_count:]
    if len(responses[efd]) == 0:
        server_epoll.modify(efd, select.EPOLLIN)

server_socket = socket.socket()
server_epoll = select.epoll()
poll = ThreadPool(512)

def put_poll(job, arg):
    poll.map(job, arg)

def main():
    server_socket.setblocking(False)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(MAX_LISTEN)

    server_epoll.register(server_socket, select.EPOLLIN)

    while True:
        events = server_epoll.poll(1) # timeout 1 sec
        for efd, estat in events:
            if efd == server_socket.fileno():
                put_poll(handle_connect, (server_socket,))
            elif estat & select.EPOLLHUP:
                put_poll(handle_diconnect, (efd,))
            elif estat & select.EPOLLIN:
                put_poll(handle_in, (efd,))
            elif estat & select.EPOLLOUT:
                put_poll(handle_out, (efd,))

if __name__ == '__main__':
    main()
