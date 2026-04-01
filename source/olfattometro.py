import time
import serial.tools.list_ports

from source.utils import get_serial_port

DEBUGGING = False

import serial
from psychopy import core, logging

class SerialWrapper:
    """
    A wrapper class for managing serial communication with a specified port and baud rate.

    Attributes:
        serial_interface (serial.Serial or None): The serial interface used for communication, or None if debugging is enabled.
        debugging (bool): A flag to enable/disable serial communication while keeping well-formatted output to the console.

    Methods:
        write(message): Prints a message to the console and optionally sends it to the serial device if debugging is disabled.
        read(wait_string): Reads data from the serial interface until a specified string is found.
                           If no string is provided, the function breaks after reading one line.
                           If debugging is enabled, serial communication is bypassed, and the function exits after the first line.
    """

    def __init__(self, port_name: str = None, baud_rate: int = 9600, debugging: bool = False):
        """
        Initializes the SerialWrapper instance with the specified port, baud rate, and debugging flag.

        If debugging is enabled, the serial interface is not initialized, and no communication will occur,
        but console output is still active.

        Args:
            port_name (str, optional): The name of the serial port (e.g., 'COM1' or '/dev/ttyUSB0'). Defaults to the result of `get_serial_port()`.
            baud_rate (int, optional): The baud rate for serial communication (e.g., 9600, 115200). Defaults to 9600.
            debugging (bool, optional): A flag to enable/disable serial communication while keeping well-formatted output to the console. Defaults to False.
        """
        if port_name is None and not debugging:
            port_name = get_serial_port()
        self.serial_interface: serial.Serial = serial.Serial(port_name, baud_rate) if not debugging else None
        self.debugging = debugging

    def write(self, message: str):
        """
        Prints a message to the console and optionally sends it to the serial device if debugging is disabled.

        Args:
            message (str): The message to be sent to the serial device.

        If debugging is enabled, the message is only printed to the console. If debugging is disabled,
        the message is sent to the serial device as well.
        """
        print('\033[32mPython: \033[0m' + message)
        if not self.debugging:
            self.serial_interface.write(bytes(message + '\r', 'utf-8'))

    def read(self, waitstring: str = None):
        """
        Reads data from the serial interface line by line until a specified string is found,
        or indefinitely if no string is specified.

        If debugging is enabled, the serial communication is bypassed, and the function exits after reading one line.

        Args:
            waitstring (str, optional): The string to wait for in the serial output.
                                         If None, the function will break after reading one line.

        Logs each line read from the serial interface for debugging if debugging is enabled.
        """
        while True:
            if self.debugging:
                print("\033[34mSniff0: \033[0m Debugging is enabled, no serial communication.")
                break

            line: str = self.serial_interface.readline().decode('utf-8', errors='ignore').strip()
            print("\033[34mSniff0: \033[0m", line)
            if waitstring is None:
                break
            if waitstring in line:
                break



class Olfactometer:
    def __init__(self,
                 timer,
                 port_name=get_serial_port(),
                 baud_rate=9600,
                 num_channels=5,
                 flusso=2.5,
                 cleanair_channel=0,
                 debugging = False,
                 screenHz = 60):
        self.port_name = port_name  #ridondante?
        self.baud_rate = baud_rate  #ridondante?
        self.num_channels = num_channels
        self.lista_canali = range(num_channels)  # [0, 1, 2, 3, 4]
        self.serial_interface = SerialWrapper(debugging=debugging)
        self.flusso = flusso
        self.stimuli_families = []  #TODO: vedere se è utile
        self.cleanair_channel = cleanair_channel
        self.serial_interface.read(waitstring='*RDY')
        core.wait(1)
        #setting the right clean air channel
        self.set_cleanair_channel(cleanair_channel)
        self.timer = timer
        self.static_period = core.StaticPeriod(screenHz=screenHz)

    def write(self, message, waitstring=None):
        self.serial_interface.write(message)
        if waitstring is not None:
            self.serial_interface.read(waitstring)

    def set_cleanair_channel(self, channel):
        message = "setCAChannel " + str(channel) + "\n"
        print(message)
        self.write(message, str(channel))

    def clean_air_on(self):
        self.set_channel(self.cleanair_channel)  #setchannel zero
        core.wait(0.010)
        message = "setValve 1\n"
        self.write(message)

    def calibration(self):
        message = "setFlow "
        for channel in self.lista_canali:
            message += (str(channel) + ":" + str(self.flusso))
            if channel != self.lista_canali[-1]:
                message += ";"
        message += "\n"
        self.write(message, '*OK')

    def flush(self,flush_duration):
        message = ''
        self.write('EnableAllValves',None)
        time.sleep(flush_duration)
        self.write('disableAllValves',None)


    def stop_calibration(self):
        message = "stopCalibration\n"
        self.write(message)

    def set_experiment(self):
        message = "setExperiment 1\n"
        self.write(message)

    def set_channel(self, channel: int):
        assert channel < self.num_channels, f'You tried to initialize a non active channel {channel}'
        message = "setChannel " + str(channel) + "\n"
        self.write(message)

    def odore_on(self, duration: int):
        #DURATION IN MILLISECONDS
        self.static_period.start(duration)
        assert duration > 0.050, f'stimulus duration too short:{duration} < 50ms'
        assert duration < 30, f"stimulus duration too long:{duration} > 30'000ms"
        message = "CfOffOpenValveTimed " + str(duration*1000) + "\n"
        self.write(message)
        self.static_period.complete()

    def test_delay(self): #TODO: SALVARE SU FILE IL TESTDELAY
        for channel in range(self.num_channels):
            message = "testDelay " + str(channel)
            self.write(message, 'AvC')

    def do_nothing(self, duration):
        core.wait(duration + 0.002)
    def openvalve(self):
        self.write('setValve 1')
    def stimulus_on(self, channel: int, stim_duration, stop_duration, repetition: int):
        '''
        UDM: millisecondi!
        La fase on di uno stimolo è comprensiva di impulsi di erogazione intervallati da periodi di
        rest, ripetuti fino alla fine della durata totale dello stimolo.
        simulus_on: (1 secondo on, 2 off) x 4 volte = 12 secondi
        :param stim_duration: la durata dell'erogazione
        :param stop_duration: la durata dell'intervallo fra le erogazioni
        :param repetition: quante volte (stim_duration + stop_duration) vanno ripetuti nell'intera fase
        :return:
        '''
        self.set_channel(channel)
        for i in range(repetition):  #[0,1,2,3] if repetition = 4
            logging.exp(f"SNIFF {self.timer.getTime():.4f} {channel} ")
            self.odore_on(stim_duration)
            if stop_duration > 0:
                logging.exp(f"ISI {self.timer.getTime():.4f}")
                self.do_nothing(stop_duration)
        return (stim_duration + stop_duration) * repetition  #milliseconds

    def cont_stimulus_on(self, channel: int, stim_duration, stop_duration, repetition: int):
        '''
        UDM: millisecondi!
        La fase on di uno stimolo è comprensiva di impulsi di erogazione intervallati da periodi di
        rest, ripetuti fino alla fine della durata totale dello stimolo.
        simulus_on: (1 secondo on, 2 off) x 4 volte = 12 secondi
        :param stim_duration: la durata dell'erogazione
        :param stop_duration: la durata dell'intervallo fra le erogazioni
        :param repetition: quante volte (stim_duration + stop_duration) vanno ripetuti nell'intera fase
        :return:
        '''
        self.set_channel(channel)
        self.odore_on((stim_duration + stop_duration)*repetition)
        return (stim_duration + stop_duration) * repetition  #milliseconds