#!/usr/bin/env python3

import message_pb2
import socket
import threading
import queue
import time


class TCPClient():
    def __init__(self, ip: str, port: int, sender: str) -> None:
        self.header = 64
        self.port = port
        self.ip = ip    # socket.gethostbyname(socket.gethostname())
        self.sender = sender
        self.address = (self.ip, self.port)
        self.header_format = 'utf-8'
        dmsg = message_pb2.Message()
        dmsg.disconnect = True
        self.disconnect_msg = dmsg
        self.client = None
        self.active = False
        self.message_queue = queue.Queue()

    def connect(self) -> None:
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.address)
            msg = message_pb2.Message()
            self.send(msg)  # Allows the server to store the name of this client
            thread = threading.Thread(target=self.__receive)
            thread.start()
            self.active = True
        except:
            print(f"[TCPClient] Could not establish connection to server {self.address}")

    def send(self, msg: message_pb2.Message, sender=None, dst="all"):
        if sender is None:
            msg.sender = self.sender
        else:
            msg.sender = sender
        msg.destination = dst
        data = msg.SerializeToString()
        msg_length = len(data)
        send_length = str(msg_length).encode(self.header_format)
        send_length += b' ' * (self.header - len(send_length))
        self.client.send(send_length)
        self.client.send(data)

    def __receive(self) -> None:
        connected = True
        while connected:
            msg_length = self.client.recv(self.header).decode(self.header_format)
            if msg_length:
                msg_length = int(msg_length)
                data = self.client.recv(msg_length)
                msg = message_pb2.Message()
                msg.ParseFromString(data)
                if msg.disconnect:
                    connected = False
                else:
                    self.message_queue.put(msg)
        self.active = False
        self.client.close()

    def get_messages(self) -> list:
        buf = []
        # Reads all messages in queue in FIFO manner
        while not self.message_queue.empty():
            buf.append(self.message_queue.get())
        return buf


if __name__ == "__main__":
    client = TCPClient(ip="127.0.0.1", port=5051, sender="autonomy")
    client.start()
    msg = message_pb2.Message()
    client.send(msg=msg, dst="hal")
    while client.active:
        messages = client.get_messages()
        for msg in messages:
            print(f"Received: {msg}")
            time.sleep(2)
            client.send(client.disconnect_msg, dst="hal")