import time
import serial
import threading
import message_pb2 as proto

class Arduino():
    def __init__(self, port: str, baudrate: int) -> None:
        self.port = port
        self.baudrate = baudrate
        self.conn = None
        self.messages = []
        self.__connect()

    def translate_proto_to_serial(self, msg: proto.Message) -> str:
        # All serial commands are csv format (cmd type, val1, val2..., val n)
        # This function needs to be carefully maintained until a better method is implemented
        if msg.HasField("command"):     # TODO: make this capable of handling multi-commands
            if msg.command.HasField("set_servo_position"):
                return f"1,{msg.command.set_servo_position.servo_pos}"
            if msg.command.HasField("set_fan_speed"):
                return f"2,{msg.command.set_fan_speed.fan_speed}"
            if msg.command.HasField("set_fan_state"):
                return f"3,{int(msg.command.set_fan_state.fan_state)}"
        if msg.HasField("telemetry"):
            pass
        if msg.HasField("config_params"):
            return f"0,{msg.config_params.telemetry_freq}"
        return None

    def translate_serial_to_proto(self, serial_buf):
        serial = serial_buf.split(',')
        msg = proto.Message()
        tlm = proto.Telemetry()
        if serial[0] == '0':  # Temperature reading
            data = proto.TemperatureData()
            data.sensor_id = int(serial[1])
            data.sensor_value = float(serial[2])
            tlm.temperature_data.CopyFrom(data)
        if serial[1] == '1':
            pass
        msg.telemetry.CopyFrom(tlm)

        return msg

    def __connect(self) -> None:
        self.conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        time.sleep(2)
        receiver = threading.Thread(target=self.__receive)
        receiver.start()

    def send_msg(self, msg: proto.Message) -> None:
        buf = self.translate_proto_to_serial(msg)
        if buf is not None:
            self.conn.write(bytes(buf, 'utf-8'))

    def __receive(self):
        while True:
            while self.conn.in_waiting:
                serial_buf = self.conn.readline().decode('utf-8').rstrip()
                msg = self.translate_serial_to_proto(serial_buf)
                self.messages.append(msg)