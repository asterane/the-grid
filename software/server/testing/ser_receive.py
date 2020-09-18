import serial, time

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

time.sleep(1)

arduino.write(b'?')
arduino.write(b'-')
arduino.write(b'{')

time.sleep(1)

while True:
    data = arduino.read()
    if data:
        print(ord(data))
