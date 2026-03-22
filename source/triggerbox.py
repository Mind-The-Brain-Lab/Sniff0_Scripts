import serial
from source.utils import get_serial_port
from psychopy.hardware import keyboard
class TriggerBox:
    def __init__(self,hint:str = 'Silicon'):
        ports = serial.tools.list_ports.comports()

        ser = get_serial_port('Silicon')
        self.ser = serial.Serial(ser, 9600)
    def wait_trigger(self):
        while True:
            self.ser.write(bytearray([2]))
            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.read(2)
                    if line[0] == 1:
                        return
                    break


class FakeTriggerBox:
    def __init__(self, hint: str = 'Keyboard'):
        self.kb = keyboard.Keyboard()

    def wait_trigger(self):
        self.kb.clearEvents()
        while True:
            keys = self.kb.getKeys(keyList=['0'], waitRelease=False)
            if keys:
                return