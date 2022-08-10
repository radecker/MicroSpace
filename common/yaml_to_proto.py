"""This script reads the config file and generates a new config.proto file
"""

import ConfigLoader
import datetime

tab = "    "

type_map = {
    str : "string",
    bool : "bool",
    int : "int32",
    float : "double",
    bytes : "bytes"
}

def head(file):
    file.write("// AUTO-GENERATED -- DO NOT MODIFY -- AUTO-GENERATED\n")
    file.write(f"// Generated {datetime.datetime.now()}\n\n")
    file.write("syntax = \"proto2\";\n")
    file.write("package InSECTS;\n\n")
    file.write("message ConfigParams {\n")

def tail(file):
    file.write("}")


if __name__=="__main__":
    config_fp = "/home/jhu-ep/InSECTS-Ground-System/main_service/config.yaml"
    cl = ConfigLoader.ConfigLoader(config_path=config_fp)
    data = cl.read_config()

    file = open("config.proto", 'w')

    head(file)
    num = 1
    for key, value in data.items():
        file.write(f"{tab}optional {type_map[type(value)]} {str(key)} = {str(num)};\n")
        num += 1
    tail(file)
    file.close()