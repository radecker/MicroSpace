#!/usr/bin/env python3

import queue
from BaseApp import BaseApp
import message_pb2 as proto
import time
import statistics
# import csv
# import numpy as np


# Autonomy Rules
#
# initial: fan speed @ 25%
# initial: baffle = closed
#
# if average temp >95C @ 25% speed, increase fan speed to 50%
# if single temp is >100C @25% speed, increase fan speed to 50%

# if average temp >100C @ 50% speed, increase fan speed to 75%
# if single tmep is >105C @25% speed, increase fan speed to 50%

# if average temp >105C @ 75% speed, increase fan speed to 100%
# if single tmep is >110C @25% speed, increase fan speed to 50%
#
# if average temp <95C @50% speed, decrease fan speed to 25%
#bla

# if average temp <100C @75% speed, decrease fan speed to 50%
#

# if average temp <105C @100% speed, decrease fan speed to 75%
#

# if fan (0) OR servomotor (1) temp >50C @ baffle = closed, set baffle = half-open
# if fan OR servomotor temp >50C @ baffle = half-open, set baffle = full-open
#
# if fan OR servomotor temp <0C @ baffle = full-open, set baffle = half-open
# if fan OR servomotor temp <0C @ baffle = half-open, set baffle = closed

# CSV Formate (FOR CODE TO WORK)
# X axis sensor 0 to sensor 5 
# Y axis sensor temp time taken 
# 1 output every second from each sensor 1 through 5


class AutonomyApp (BaseApp):
    def __init__(self) -> None:
        self.baffle = 0     # 0 is closed 1 is half 2 is open
        self.fanspeed = 1   # 0 is off 1 is 25% 2 is 50% 3 is 75% 4 is 100%
        self.manual_mode = None
        self.temp_data = dict()
        super().__init__("vehicle.autonomy_app")
        
    def read_tempSensors(self):
        for msg in self.telemetry_queue:
            if msg.HasField("telemetry"):
                if msg.telemetry.HasField("temperature_data"):
                    sensor_id = msg.telemetry.temperature_data.sensor_id
                    if sensor_id not in self.temp_data:
                        self.temp_data[sensor_id] = []
                        self.temp_data[sensor_id].append(msg.telemetry.temperature_data.sensor_value)
                    elif len(self.temp_data[sensor_id]) >= 5:
                        self.temp_data[sensor_id].pop(0)
                        self.temp_data[sensor_id].append(msg.telemetry.temperature_data.sensor_value)
                    else:
                        self.temp_data[sensor_id].append(msg.telemetry.temperature_data.sensor_value)
        # tempSensors = []
        # AveSingeSensorTemp = []
        # with open(self.csv,mode = 'r') as file:
        #     csvFile = csv.reader(file)
        #     counter = 0 
        #     for lines in csvFile:
        #         if counter == 0:
        #             counter = 1 
        #         else : # Takes last 5 seconds of data for max & average
        #             l=len(lines)
        #             AveSingeSensorTemp.append(int(lines[l-5]))
        #             AveSingeSensorTemp.append(int(lines[l-4]))
        #             AveSingeSensorTemp.append(int(lines[l-3]))
        #             AveSingeSensorTemp.append(int(lines[l-2]))
        #             AveSingeSensorTemp.append(int(lines[l-1]))
        #             tempSensors.append(statistics.mean(AveSingeSensorTemp))
        #             AveSingeSensorTemp = []
        #     return tempSensors #return array 
        
    def send_fanspeed_and_baffle(self):
        msg = proto.Message()
        cmd = proto.Command()
        fan_cmd = proto.SetFanSpeed()
        fan_cmd.fan_speed = self.fanspeed
        cmd.set_fan_speed.CopyFrom(fan_cmd)
        msg.command.CopyFrom(cmd)
        print(msg)
        self.send_command(msg)

        msg = proto.Message()
        cmd = proto.Command()
        servo_cmd = proto.SetServoPosition()
        servo_cmd.servo_pos = self.baffle
        cmd.set_servo_position.CopyFrom(servo_cmd)
        msg.command.CopyFrom(cmd)
        self.send_command(msg)
        print(msg)
            
    def setup(self) -> None:
        self.manual_mode = False
        print("Autonomy System Online")
    
    def run(self) -> None:
        # Read commands and telem
        if len(self.command_queue):
            pass
        if len(self.telemetry_queue):
            self.read_tempSensors()
        if not self.manual_mode:
            alltemps = []
            for sensor in self.temp_data.values():
                for temp in sensor:
                    alltemps.append(temp)
            if len(alltemps) > 2:
                if statistics.mean(alltemps) > 95 and self.fanspeed == 25: 
                    self.fanspeed = 50
                elif statistics.mean(alltemps) > 100 and self.fanspeed == 50: 
                    self.fanspeed = 75
                elif statistics.mean(alltemps) > 105 and self.fanspeed == 75: 
                    self.fanspeed = 100
                elif statistics.mean(alltemps) < 95 and self.fanspeed >= 50: 
                    self.fanspeed = 25
                elif statistics.mean(alltemps) < 100 and self.fanspeed >= 75: 
                    self.fanspeed = 50
                elif statistics.mean(alltemps) < 105 and self.fanspeed == 100: 
                    self.fanspeed = 75
                        
                if max(alltemps) > 100 and self.fanspeed == 25:
                    self.fanspeed = 50
                elif max(alltemps) > 105 and self.fanspeed == 50:
                    self.fanspeed = 75
                elif max(alltemps) > 110 and self.fanspeed == 75:
                    self.fanspeed = 100
                elif max(alltemps) < 100 and self.fanspeed >= 50:
                    self.fanspeed = 25
                elif max(alltemps) < 105 and self.fanspeed >= 75:
                    self.fanspeed = 50
                elif max(alltemps) < 110 and self.fanspeed == 100:
                    self.fanspeed = 75

                if (alltemps[0] > 50 or alltemps[1] > 50) and self.baffle == 0: 
                    self.baffle = 1
                elif (alltemps[0] > 55 or alltemps[1] > 55) and self.baffle == 1: 
                    self.baffle = 2
                elif (alltemps[0] < 50 or alltemps[1] < 50) and self.baffle >= 1: 
                        self.baffle = 0
                elif (alltemps[0] < 55 or alltemps[1] < 55) and self.baffle == 2: 
                        self.baffle = 1
                    
                self.send_fanspeed_and_baffle()
                time.sleep(5)

if __name__ == "__main__":
    a= AutonomyApp()
    # a.run() # Runs the app
    
