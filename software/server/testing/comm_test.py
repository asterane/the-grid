import serial, time


def setChannel(target: serial.Serial, count, header, channel, intensity):
    packet = bytearray(2)

    if (channel < 1) or (channel > count) or \
            (intensity < 0) or (intensity > 255):
        raise ValueError("A channel or intensity parameter was invalid.")

    target.reset_input_buffer()

    packet[0] = channel
    packet[1] = intensity

    target.write(header)
    target.write(packet)

    time.sleep(0.05)

    if target.in_waiting > 0:
        feedback = target.read()
        return ord(feedback) == packet[1]
    else:
        return False


arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=5)
arduino.reset_input_buffer()
time.sleep(1)

data = arduino.readline()[:-2]
if data:
    print("Arduino says: " + data.decode())

chanCount = arduino.read()
chanCount = ord(chanCount)

packetStart = b'?'

while True:
    try:
        try:
            channel = int(input("\nChoose Channel (1 - %i): " % chanCount))
            intensity = int(input("Select Intensity (0 - 255): "))

            if setChannel(arduino, chanCount, packetStart, channel, intensity):
                print("Success!")
            else:
                print("Success not guaranteed.")

        except ValueError:
            print("Try again.")
            continue

        for i in range(0, arduino.in_waiting):
            newData = arduino.read()
            print(ord(newData))

    except KeyboardInterrupt:
        print('\n')
        break
