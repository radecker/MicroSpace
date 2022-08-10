#!/usr/bin/env python3

from TCPClient import TCPClient
from UDPClient import UDPClient
from BaseApp import BaseApp
import message_pb2 as proto
import boto3
import threading
import datetime
import time


class CloudService(BaseApp):
    def __init__(self) -> None:
        self.command_table = None
        self.telem_table = None
        self.client = None
        super().__init__("ground.cloud_service")

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id':"1"
            }
        )
        return response

    def put(self, Sensor_Id='' , Temperature='' , Date='' , Time=''):
        self.telem_table.put_item(
            Item={
                'Sensor_Id':Sensor_Id,
                'Temperature':Temperature,
                'Date' :Date,
                'Time' :Time
            }
        )

    def delete_command(self, request_number):
        self.command_table.delete_item(
            Key={
                'Request_Number': request_number
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='Sensor'
        )
        return response

    def push_to_cloud(self, msg: proto.Message):
        id = msg.telemetry.temperature_data.sensor_id
        temp = msg.telemetry.temperature_data.sensor_value
        now = datetime.datetime.now()
        date=now.strftime('%Y-%m-%d')
        ctime=now.strftime('%H:%M:%S %Z')
        if self.config_params.connect_to_telemetry_database:
            self.put(Sensor_Id=str(id), Temperature=str(temp), Date=str(date), Time=str(ctime))
        print(f"Uploaded Sample on Cloud Id:{id} T:{temp} D:{date} T:{ctime}")

    def setup(self):
        if self.config_params.connect_to_command_database:
            self.db = boto3.resource('dynamodb', region_name='us-east-1')
            self.command_table = self.db.Table(self.config_params.command_database_name)
            print("[Connected to command table]")
        if self.config_params.connect_to_telemetry_database:
            self.telem_table = self.db.Table(self.config_params.telemetry_database_name)
            self.client = boto3.client('dynamodb')
            print("[Connected to telemetry table]")
        else:
            pass
    
    def get_commands(self):
        reading = self.command_table.scan()
        
        return reading['Items']

    def translate_command(self, command):
        print(command)
        msg = proto.Message()
        cmd = proto.Command()
        if "Autonomy_status" in command.keys():
            scmd = proto.SetAutonomyState()
            scmd.autonomy_state = bool(int(command["Autonomy_status"]))
            cmd.set_autonomy_state.CopyFrom(scmd)
            msg.command.CopyFrom(cmd)
            print(msg)
            self.send_command(msg)
        msg = proto.Message()
        cmd = proto.Command()
        if "Fan_Speed" in command.keys():
            scmd = proto.SetFanSpeed()
            scmd.fan_speed = int(command["Fan_Speed"])
            cmd.set_fan_speed.CopyFrom(scmd)
            msg.command.CopyFrom(cmd)
            print(msg)
            self.send_command(msg)
        msg = proto.Message()
        cmd = proto.Command()
        if "Trim_Position" in command.keys():
            scmd = proto.SetServoPosition()
            scmd.servo_pos = int(command["Trim_Position"])
            cmd.set_servo_position.CopyFrom(scmd)
            msg.command.CopyFrom(cmd)
            print(msg)
            self.send_command(msg)
        self.delete_command(command["Request_Number"])

    def run(self):
        # Grab the latest telemetry and push to database
        if len(self.telemetry_queue):
            for msg in self.telemetry_queue:
                if msg.HasField("telemetry"):
                    self.push_to_cloud(msg)

        commands = self.get_commands()
        # print(commands)
        for i in range(0,len(commands)):
            self.translate_command(commands[i])
        time.sleep(2)
        

    def shutdown(self):
        pass


if __name__ == "__main__":
    CloudService()   # Runs the service
    