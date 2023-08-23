import serial


class Marker:
    def __init__(self, port="COM1", timeout=0.1, badurate=115200):
        self.ser = serial.Serial(port=port, timeout=timeout, baudrate=badurate)

    def __del__(self):
        self.ser.close()


if __name__ == '__main__':
    pass
