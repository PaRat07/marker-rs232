import serial
import time


class Marker:
    def __write_to_marker(self, message):
        self.ser.write(bytes(message + ';;', 'utf-8'))
        time.sleep(1)

    def __read_from_marker(self) -> str:
        ans = ""
        postfix = self.ser.read(2).decode()
        while postfix != ';;':
            ans += postfix[0]
            postfix = postfix[1] + self.ser.read().decode()

        return ans

    def __init__(self, port="COM5", timeout=0.1, badurate=9600):
        self.ser = serial.Serial(port=port, timeout=timeout, baudrate=badurate)

    def __del__(self):
        self.ser.close()

    def get_status(self) -> int:
        self.__write_to_marker('GetMarkStatus')
        return int(self.__read_from_marker())

    def set_pen_parameter(self, pen_id=0, mark_speed=1000, power=100):
        self.__write_to_marker('SetPen,ID,' + str(pen_id) + ';MarkSpeed,' + str(mark_speed) + ';Power,' + str(power))
        time.sleep(0.5)
        print('Settings pen:', self.__read_from_marker())

    def open_doc(self, file: str):
        self.__write_to_marker('OpenDoc,' + file)
        print('OpenDoc:', self.__read_from_marker())

    def mark_file(self, file: str):
        self.set_pen_parameter()
        self.open_doc(file)
        self.__write_to_marker('StartMark')
        print('Start mark:', self.__read_from_marker())
        time.sleep(5)
        self.__write_to_marker('StopMark')
        print('StopMark:', self.__read_from_marker())

    def change_file_content(self, file: str, content: str):
        self.open_doc(file)
        self.__write_to_marker('GetShapeList')
        primitives = self.__read_from_marker().split(';')
        message = 'SetShapeData,'
        for i in primitives:
            self.__write_to_marker('GetShapePos,' + i)
            data = self.__read_from_marker().split(',')
            self.__write_to_marker('SetShapeData,' + str(i) + ',' + content)
            print('SetShapeData: ' + self.__read_from_marker())
            self.__write_to_marker('GetShapePos,' + i)
            data1 = self.__read_from_marker().split(',')
            x_offset = (float(data[1]) + float(data[3]) / 2) - (float(data1[1]) + float(data1[3]) / 2)
            y_offset = (float(data[2]) + float(data[4]) / 2) - (float(data1[2]) + float(data1[4]) / 2)
            self.__write_to_marker('SetShapeData,' + str(i) + ',,' + str(x_offset) + ',' + str(y_offset) + ',0')
            print('SetShapeData: ' + self.__read_from_marker())
        self.__write_to_marker('SaveCurrentDoc')
        print('SaveCurrentDoc:' + self.__read_from_marker())


if __name__ == '__main__':
    m = Marker()
    m.change_file_content('test.bpd', 'PaRat07')
    m.mark_file('test.bpd')
