#!/usr/bin/env python3

import queue
import message_pb2 as proto
import socket 
import threading
import time
import queue
import struct

"""
Ways this can be improved:
    1. Method to close a connection or shutdown a sender/listener
    2. Algo Optimization
    3. More straightforward API
"""


class UDPClient():
    def __init__(self, id: str) -> None:
        self.id = id
        self.listen_all = False

        # Dictionary of queues used to maintain sender/listener ID capability
        self.__receive_queues = dict()
        
        self.__sock = None
        self.__address = None
        self.__send_queues = dict()
        self.__header_len = 64
        self.__header_format = 'utf-8'

    def add_listener(self, group: str, port: int) -> None:
        self.__receive_queues[(group, port)] = queue.Queue()
        thread = threading.Thread(target=self.__add_listener, args=(group, port))
        thread.start()

    def __add_listener(self, group: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.listen_all:
            sock.bind(('', port))
        else:
            sock.bind((group, port))
        mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.__receive(sock, group, port)

    def __receive(self, sock, group, port) -> None:
        while True:
            msg_len = sock.recv(self.__header_len).decode(self.__header_format)
            if msg_len:
                data = sock.recv(int(msg_len))
                msg = proto.Message()
                msg.ParseFromString(data)
                self.__receive_queues[(group, port)].put(msg)
        sock.close()

    def send(self, msg: proto.Message, group: str, port: int, sender=None, destination="all") -> None:
        if sender is None:
            msg.sender = self.id
        else:
            msg.sender = sender
        msg.destination = destination
        if not (group, port) in self.__send_queues:
            print(f"[UDP Client] ERROR: first add sender on {group, port}")
        else:
            self.__send_queues[(group, port)].put(msg)

    def add_sender(self, group: str, port: int) -> None:
        self.__send_queues[(group, port)] = queue.Queue()
        thread = threading.Thread(target=self.__add_sender, args=(group, port))
        thread.start()

    def __add_sender(self, group: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2) # Might need to change 2
        while True:
            if not self.__send_queues[(group, port)].empty():
                data = self.__send_queues[(group, port)].get().SerializeToString()
                msg_len = len(data)
                send_length = str(msg_len).encode(self.__header_format)
                send_length += b' ' * (self.__header_len - len(send_length))
                sock.sendto(send_length, (group, port))
                sock.sendto(data, (group, port))

    def get_messages(self, group=None, port=None) -> list:
        buf = []
        if group is None and port is None:
            for key in self.__receive_queues.keys():
                while not self.__receive_queues[key].empty():
                    buf.append(self.__receive_queues[key].get())
            return buf
        if group and port:
            if not (group, port) in self.__receive_queues:
                print(f"[UDP Client] ERROR: first add listener on {group, port}")
            else:
                while not self.__receive_queues[(group, port)].empty():
                    buf.append(self.__receive_queues[(group, port)].get())
                return buf
        return None


if __name__ == "__main__":
    print("[UDP Client] starting up...")
    client = UDPClient(id="UDPClientTest")
    client.add_listener(group="224.1.1.1", port=5050)
    time.sleep(2)
    client.add_sender(group="224.1.1.1", port=5050)
    msg = proto.Message()
    client.send(msg, group="224.1.1.1", port=5050)
    while True:
        messages = client.get_messages(group="224.1.1.1", port=5050)
        for msg in messages:
            print(f"Message: {msg}")