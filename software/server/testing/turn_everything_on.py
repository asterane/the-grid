import arduino

import time

try:
    mega = [arduino.Arduino('/dev/ttyACM0', b'?'), arduino.Arduino('/dev/ttyACM1', b'?'), arduino.Arduino('/dev/ttyACM2', b'?'), arduino.Arduino('/dev/ttyACM3', b'?')]
except:
    print('Unable to connect.\n')
    exit()

print('Connected!\n')
for i in mega:
    print(i.connect())
    i.getChanCount()
    i.reset()

while True:
    total = 0
    try:
        intensity = int(input("Select Intensity (0 - 255): "))

        for i in mega:
            for j in range(1, 47):
                total += 3
                if total >= 63:
                    time.sleep(0.1)
                    total = 0
                i.setChannel(j, intensity, False)

    except KeyboardInterrupt:
        print('\n')
        exit()
