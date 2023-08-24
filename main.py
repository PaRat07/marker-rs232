import serial
import time


class Marker:
    def __write_to_marker(self, message):
        self.ser.write(bytes(message + ';;', 'utf-8'))

    def __read_from_marker(self) -> str:
        ans = ""
        postfix = self.ser.read(2).decode()
        while postfix != ';;':
            ans += postfix[0]
            postfix = postfix[1] + self.ser.read().decode()

        return ans

    def __init__(self, port="COM5", timeout=0.1, badurate=115200):
        self.ser = serial.Serial(port=port, timeout=timeout, baudrate=badurate)

    def __del__(self):
        self.ser.close()

    def set_pen_parameter(self, pen_id=0, mark_speed=1000, power=100):
        self.__write_to_marker('SetPen,ID,' + str(pen_id) + ';MarkSpeed,' + str(mark_speed) + ';Power,' + str(power))
        time.sleep(0.5)
        print('Settings pen:', self.__read_from_marker())

    def mark(self, file: str):
        self.__write_to_marker('OpenDoc,' + file)
        print('OpenDoc:', self.__read_from_marker())
        self.set_pen_parameter()
        self.__write_to_marker('StartMark')
        print('Start mark:', self.__read_from_marker())
        time.sleep(0.5)
        self.__write_to_marker('StopMark')
        print('StopMark:', self.__read_from_marker())


if __name__ == '__main__':
    m = Marker()
    m.mark('test.bpd')
