#!/usr/bin/env python3

from UDPClient import UDPClient

import message_pb2 as proto
import socket
import threading
import queue
import time

"""
General sequence:
    1. Connect to infrastructure multicast group
    2. Listen for config params and read them in
    3. perform ack that all apps see each other (skip for now)
    4. Call Setup with startup params as message input
    5. Call Run
"""

"""
Todo:
    1. Add scheduled send
    2. Add some sort of routing class
"""

class BaseApp():
    def __init__(self, id: str) -> None:
        self.udp_client = UDPClient(id=id)
        self.config_params = None
        self.command_queue = []
        self.telemetry_queue = []

        self.__startup_group = "224.1.1.90"
        self.__startup_port = 5090
        self.__command_group = None
        self.__command_port = None
        self.__telemetry_group = None
        self.__telemetry_port = None

        self.__initialize()
        self.setup()
        while True:
            self.command_queue = self.udp_client.get_messages(self.__command_group, self.__command_port)
            self.telemetry_queue = self.udp_client.get_messages(self.__telemetry_group, self.__telemetry_port)
            self.run()

    def __initialize(self):
        """Sets up connection and listens for init params from main controller
        """
        self.udp_client.add_listener(group=self.__startup_group, port=self.__startup_port)
        self.udp_client.add_sender(group=self.__startup_group, port=self.__startup_port)
        self.__wait_for_config_params()
        self.__ack_config()
        self.__connect_command_group()
        self.__connect_telemetry_group()

    def __wait_for_config_params(self) -> None:
        """Waits until config params have been received
        """
        while self.config_params is None:
            request = proto.Message()
            request.request_config = True
            self.udp_client.send(request, group=self.__startup_group, port=self.__startup_port, destination="main_service")
            time.sleep(1)
            messages = self.udp_client.get_messages()
            for message in messages:
                if message.HasField("config_params"):
                    self.config_params = message.config_params

    def __ack_config(self):
        msg = proto.Message()
        msg.ack = True
        self.udp_client.send(msg, self.__startup_group, self.__startup_port, destination="main_service")

    def __connect_command_group(self):
        """Setup connection and start listening for any commands
        """
        self.__command_group = self.config_params.command_multicast_ip
        self.__command_port = self.config_params.command_multicast_port
        self.udp_client.add_listener(group=self.__command_group, port=self.__command_port)
        self.udp_client.add_sender(group=self.__command_group, port=self.__command_port)

    def __connect_telemetry_group(self):
        """Setup connection and start listening for any telemetry
        """
        self.__telemetry_group = self.config_params.telemetry_multicast_ip
        self.__telemetry_port = self.config_params.telemetry_multicast_port
        self.udp_client.add_listener(group=self.__telemetry_group, port=self.__telemetry_port)
        self.udp_client.add_sender(group=self.__telemetry_group, port=self.__telemetry_port)

    def send_command(self, msg: proto.Message, sender=None, destination="all"):
        self.udp_client.send(msg, self.__command_group, self.__command_port, sender, destination)

    def send_telemetry(self, msg: proto.Message, sender=None, destination="all"):
        self.udp_client.send(msg, self.__telemetry_group, self.__telemetry_port, sender, destination)

    def setup(self):
        """Runs once prior to Run() loop
        """
        raise NotImplementedError()

    def run(self):
        """runs in a loop continously
        """
        raise NotImplementedError()

    def shutdown(self):
        """Called when the system shuts down
        """
        raise NotImplementedError()


if __name__=="__main__":
    base_app = BaseApp("base_app")
    print(f"params {base_app.config_params}")