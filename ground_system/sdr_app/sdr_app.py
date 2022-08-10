#!/usr/bin/env python3

from BaseApp import BaseApp
from TCPServer import TCPServer
import message_pb2 as proto
import time
import queue

"""
Purpose: This app is used to connect the ground system to the vehicle via SDR or simulation
"""

class SDRApp(BaseApp):
    def __init__(self) -> None:
        self.tcp_server = None
        self.tcp_send_queue = queue.Queue()
        super().__init__("ground.sdr_app")

    def setup(self):
        ip = self.config_params.sdr_tcp_server_ip
        port = self.config_params.sdr_tcp_server_port
        self.tcp_server = TCPServer(ip=ip, port=port, sender="ground.sdr_app")
        self.tcp_server.start()

    def run(self):
        if len(self.command_queue) and "vehicle.sdr_app" in self.tcp_server.connections:
            for msg in self.command_queue:
                if "vehicle." in msg.destination or "all" == msg.destination:
                    if "ground.sdr_app" not in msg.sender:
                        self.tcp_server.send(msg=msg, dst=msg.destination, client="vehicle.sdr_app")
        if len(self.telemetry_queue) and "vehicle.sdr_app" in self.tcp_server.connections:
            for msg in self.telemetry_queue:
                if "vehicle." in msg.destination or "all" == msg.destination:
                    if "ground.sdr_app" not in msg.sender:
                        self.tcp_server.send(msg=msg, dst=msg.destination, client="vehicle.sdr_app")
        if not self.tcp_server.message_queue.empty():
            msg = self.tcp_server.message_queue.get()
            if msg.HasField("command"):
                self.send_command(msg, sender=msg.sender, destination=msg.destination)
            if msg.HasField("telemetry"):
                self.send_telemetry(msg, sender=msg.sender, destination=msg.destination)
            

    def shutdown(self):
        pass


if __name__ == "__main__":
    SDRApp()