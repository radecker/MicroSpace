#!/usr/bin/env python3

from BaseApp import BaseApp
import datetime
import time


class LoggerService(BaseApp):
    def __init__(self) -> None:
        self.log = None
        super().__init__("ground.logger_service")

    def setup(self):
        print(self.config_params)
        self.log = open(f"network_traffic.log", 'w')

    def run(self):

        if len(self.telemetry_queue):
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S %Z')
            print(date + time)
            print(self.telemetry_queue.pop())
        if len(self.command_queue):
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S %Z')
            print(date + time)
            print(datetime.datetime.now().ctime())
            print(self.command_queue.pop())

if __name__ == "__main__":
    LoggerService()   # Runs the app