import serial
import serial

# Replace 'COM3' with your serial port name.

from source.utils import get_serial_port
import serial.tools.list_ports

# Get a list of all available ports
ports = serial.tools.list_ports.comports()

ser = get_serial_port('Silicon')
ser = serial.Serial(ser,9600)
print('starting the test')
while True:
    ser.write(bytearray([2]))
    while True:
        if ser.in_waiting > 0:
            line = ser.read(2)
            if line[0] == 1:
                print('trigger')
            else:
                pass
            break
