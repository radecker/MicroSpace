#!/usr/bin/env python3

from TCPServer import TCPServer
from BaseApp import BaseApp
from Arduino import Arduino
import message_pb2 as proto
import queue
import serial
import time

"""
Purpose: This app is supposed to expose/emulate much of the hardware functions to the applications running

Use Cases:
    1. Abstract serial connection to arduino/wowki
    2. ????
"""



class HalService(BaseApp):
    def __init__(self) -> None:
        self.arduino = None
        super().__init__(id="ground.hal_service")

    def _send_to_arduino(self):
        if self.config_params.emulate_arduino:
            # Connect to Wowki server instead
            pass
        else:
            # Send data over serial
            pass

    def setup(self):
        config = self.config_params
        self.arduino = Arduino(port=config.arduino_address, baudrate=config.serial_baudrate)

    def run(self):
        # Send any command messages
        if len(self.command_queue):
            self.arduino.send_msg(self.command_queue.pop())
        
        # Ready any messages from arduino
        if len(self.arduino.messages):
            msg = self.arduino.messages.pop()
            print(msg)
            self.send_telemetry(msg)

    def shutdown(self):
        pass


if __name__ == "__main__":
    HalService()