import sys

import serial


def get_connection_to_arduino():
    from serial.tools.list_ports_linux import comports

    for p in comports():
        if p.description == "Arduino Uno":
            return serial.Serial(p.device)

    raise Exception("Arduino Not Found")


def keep_reading(serial_conn: serial.Serial, on_new_number):
    while True:
        try:
            line = serial_conn.readline()
            on_new_number(float(line))
        except Exception as e:
            print(e, file=sys.stderr)
