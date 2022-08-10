#!/usr/bin/env python3

from BaseApp import BaseApp
from TCPClient import TCPClient
import message_pb2 as proto
import time
import queue

"""
Purpose: This app is used to connect the ground system to the vehicle via SDR or simulation
"""

class SDRApp(BaseApp):
    def __init__(self) -> None:
        self.tcp_client = None
        self.tcp_send_queue = queue.Queue()
        super().__init__("vehicle.sdr_app")

    def setup(self):
        ip = self.config_params.sdr_tcp_client_ip
        port = self.config_params.sdr_tcp_client_port
        self.tcp_client = TCPClient(ip=ip, port=port, sender="vehicle.sdr_app")
        while not self.tcp_client.active:
            self.tcp_client.connect()
            time.sleep(2)

    def run(self):
        if len(self.command_queue):
            for msg in self.command_queue:
                if "ground." in msg.destination or "all" == msg.destination:
                    if "vehicle.sdr_app" not in msg.sender:
                        self.tcp_client.send(msg=msg, sender=msg.sender, dst=msg.destination)
        if len(self.telemetry_queue):
            for msg in self.telemetry_queue:
                if "ground." in msg.destination or "all" == msg.destination:
                    if "vehicle.sdr_app" not in msg.sender:
                        self.tcp_client.send(msg=msg, sender=msg.sender, dst=msg.destination)
        if not self.tcp_client.message_queue.empty():
            msg = self.tcp_client.message_queue.get()
            if msg.HasField("command"):
                self.send_command(msg, sender=msg.sender, destination=msg.destination)
            if msg.HasField("telemetry"):
                self.send_telemetry(msg, sender=msg.sender, destination=msg.destination)

    def shutdown(self):
        pass


if __name__ == "__main__":
    SDRApp()