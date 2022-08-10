#!/usr/bin/env python3

from BaseApp import BaseApp
import datetime
import time


class LoggerService(BaseApp):
    def __init__(self) -> None:
        self.log = None
        super().__init__("vehicle.logger_service")

    def setup(self):
        print("Logger SETUP!")
        print(self.config_params)
        self.log = open(f"network_traffic.log", 'w')

    def run(self):
        if len(self.telemetry_queue):
            print(datetime.datetime.now().ctime())
            print(self.telemetry_queue.pop())
        if len(self.command_queue):
            print(datetime.datetime.now().ctime())
            print(self.command_queue.pop())

if __name__ == "__main__":
    LoggerService()   # Runs the app