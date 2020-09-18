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
            for j in range(1, 48):
                i.setChannel(j, intensity, False)
                print(F"Board {mega.index(i)}, Channel {j} on.")
                input("Enter to proceed.")
                if i.setChannel(j, 0):
                    print("Off.")

    except KeyboardInterrupt:
        print('\n')
        exit()
