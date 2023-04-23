import serial
import time
import math

def arduino_read(data_from_arduino):
    
    arduino = serial.Serial('COM4', 115200, timeout=.1)

    try:
        arduino.open()
        if arduino.is_open:
            print('CONNECTED')
    except:
        pass
    time.sleep(1)
    while True:
        arduino.readline = lambda: arduino.read_until(b'\n').rstrip(b'\n') # get rid of \n in serial
        raw = arduino.readline()

        try:
            pos = raw.decode('utf-8').split(",")
            data_from_arduino[0] = float(pos[0])
            data_from_arduino[1] = float(pos[1])
            arduino.flush()
            # print(x_ar, y_ar)
        except:
            pass
def normalize_vector(vector):
    x, y = vector[0], vector[1]
    magnitude = math.sqrt(x**2 + y**2)
    normalized_vector = [x/magnitude, y/magnitude]
    return normalized_vector    