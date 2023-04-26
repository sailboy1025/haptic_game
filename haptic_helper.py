import serial
import time
import math
class HapkitCommute:
    def __init__(self, com, baud):
        self.arduino = serial.Serial(com, baud, timeout=.1)
    def arduino_read(self, data_from_arduino):
        
        # arduino = serial.Serial('COM5', 115200, timeout=.1)

        try:
            self.arduino.open()
            if self.arduino.is_open:
                print('CONNECTED')
        except:
            pass
        time.sleep(1)
        while True:
            self.arduino.readline = lambda: self.arduino.read_until(b'\n').rstrip(b'\n') # get rid of \n in serial
            raw = self.arduino.readline()

            try:
                pos = raw.decode('utf-8').split(",")
                data_from_arduino[0] = float(pos[0])
                data_from_arduino[1] = float(pos[1])
                data_from_arduino[2] = int(pos[2])
                self.arduino.flush()
                # print(x_ar, y_ar)
            except:
                pass
    def arduino_write(self, force_x = 0, force_y = 0, damp = 1):
        try:
            py_msg = str(force_x) + ',' + str(force_y) + ',' + str(damp)
            self.arduino.write(py_msg.encode('UTF-8'))
            print(f'{py_msg} is successfully sent to port')
        except:
            print('Something Wrong')
            pass
def normalize_vector(vector):
    x, y = vector[0], vector[1]
    magnitude = math.sqrt(x**2 + y**2)
    normalized_vector = [x/magnitude, y/magnitude]
    round_vector = [round(nv, 3) for nv in normalized_vector]
    return round_vector    