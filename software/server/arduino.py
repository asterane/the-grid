import time
import serial

class Arduino:
    def __init__(self, port:str, header:bytes):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.timeout = 1

        self.header = header
        self.chanCount = 0

    def connect(self):
        self.ser.open()
        return self.ser.is_open

    def disconnect(self):
        self.ser.close()

    def restart(self, wait=1):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.close()
        time.sleep(wait)
        self.ser.open()
        return self.ser.is_open

    def reset(self, wait=1):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        time.sleep(wait)

    def getLine(self):
        line = self.ser.readline()[:-2]
        if line:
            return line.decode()
        else:
            return ''

    def getData(self):
        data = []
        for i in range(0, self.ser.in_waiting):
            byte = self.ser.read()
            data.append(ord(byte))
        return data

    def getChanCount(self):
        try:
            self.chanCount = self.getData()[0]
        except:
            self.chanCount = 50

    def setChannel(self, channel, intensity, check=True):
        """ Set the brightness of a particular color channel.
            Accepts channel number and intensity up to 255. Checks for bad input. """
        packet = bytearray(2)

        if (channel < 1) or (channel > self.chanCount) or \
            (intensity < 0) or (intensity > 255):
            raise ValueError("A channel or intensity parameter was invalid.")

        self.reset(0)

        packet[0] = channel
        packet[1] = intensity

        self.ser.write(self.header)
        self.ser.write(packet)

        if check:
            time.sleep(0.05)

            if self.ser.in_waiting > 0:
                feedback = self.ser.read()
                if ord(feedback) == packet[1]:
                    return True
                else: return False
            else: return False
