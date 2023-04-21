import serial
import time
class GetHapkicPos():
    def __init__(self, port, baud) -> None:
        self.port = port
        self.baud = baud

    def position(self):
        arduino = serial.Serial(self.port, self.baud, timeout=.1)
        try:
            arduino.open()
            if arduino.is_open:
                print('CONNECTED')
        except:
            pass
        time.sleep(1)
        while True:

            raw = arduino.readline()
            
            try:
                pos = raw.decode('utf-8').split(',')
                return pos[0], pos[1] - '/n'
            except:
                pass
            


    

