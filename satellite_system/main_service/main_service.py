#!/usr/bin/env python3

from email import message
from TCPClient import TCPClient
from UDPClient import UDPClient
from ConfigLoader import ConfigLoader

import message_pb2
import config_pb2
import time
import subprocess

STARTUP_IP = "224.1.1.95"
STARTUP_PORT = 5095


def ConvertConfigDictToProto(config: dict) -> message_pb2.Message:
    msg = message_pb2.Message()
    config_msg = config_pb2.ConfigParams()
    for key, val in config.items():
        setattr(config_msg, key, val)
    msg.config_params.CopyFrom(config_msg)
    
    return msg


if __name__ == "__main__":
    # Load the config parameters
    configs = ConfigLoader("config.yaml").read_config()

    # Convert the config dict to a protobuf message
    config_msg = ConvertConfigDictToProto(configs)
    
    # Start execution of other core infrastructure services
    # TODO: This is only needed while K3 is not running
    # subprocess.Popen(["docker", "run", "--network=host", "autonomy_app"])
    # subprocess.Popen(["docker", "run", "--network=host", "--privileged", "logger_service"])

    # os.system("docker run --network=host autonomy_app")

    udp_client = UDPClient("main_service")
    udp_client.add_sender(group=STARTUP_IP, port=STARTUP_PORT)
    udp_client.add_listener(group=STARTUP_IP, port=STARTUP_PORT)

    while True:
        msgs = udp_client.get_messages()
        for msg in msgs:
            if msg.destination == "main_service":
                print(msg)
                if msg.HasField("request_config"):
                    udp_client.send(config_msg, group=STARTUP_IP, port=STARTUP_PORT)
        time.sleep(1)