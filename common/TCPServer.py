#!/usr/bin/env python3

import queue
import message_pb2
import socket 
import threading
import queue
import time


class TCPServer():
    def __init__(self, ip: str, port: int, sender: str) -> None:
        self.header = 64
        self.port = port
        self.ip = ip    # socket.gethostbyname(socket.gethostname())
        self.address = (self.ip, self.port)
        self.header_format = 'utf-8'
        self.sender = sender
        dmsg = message_pb2.Message()
        dmsg.disconnect = True
        self.disconnect_msg = dmsg
        self.server = None
        self.message_queue = queue.Queue()
        self.connections = dict()

    def start(self) -> None:
        thread = threading.Thread(target=self.__start)
        thread.start()

    def __start(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen()
        print(f"[SERVER] listening on {self.address}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.__handle_client, args=(conn, addr))
            thread.start()
            print(f"[SERVER] active connections = {threading.activeCount() - 2}")

    def __handle_client(self, conn, addr) -> None:
        print(f"[SERVER] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(self.header).decode(self.header_format)
            if msg_length:
                msg_length = int(msg_length)
                data = conn.recv(msg_length)
                msg = message_pb2.Message()
                msg.ParseFromString(data)
                if msg.disconnect:
                    self.send(self.disconnect_msg, msg.sender)
                    del self.connections[msg.sender]
                    connected = False
                else:
                    self.connections[msg.sender] = conn
                    self.message_queue.put(msg)
        conn.close()

    def send(self, msg: message_pb2.Message, dst: str, client: str):
        msg.sender = self.sender
        msg.destination = dst
        data = msg.SerializeToString()
        msg_length = len(data)
        send_length = str(msg_length).encode(self.header_format)
        send_length += b' ' * (self.header - len(send_length))
        conn = self.connections[client]
        conn.send(send_length)
        conn.send(data)

    def get_messages(self) -> list:
        buf = []
        # Reads all messages in queue in FIFO manner
        while not self.message_queue.empty():
            buf.append(self.message_queue.get())
        
        return buf

if __name__ == "__main__":
    print("[SERVER] starting up...")
    server = TCPServer(ip="127.0.0.1", port=5051, sender="hal")
    server.start()
    while True:
        messages = server.get_messages()
        for msg in messages:
            print(f"Message: {msg}")
            if msg.destination == "hal":
                reply = message_pb2.Message()
                server.send(msg=reply, dst=msg.sender)