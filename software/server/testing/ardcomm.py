import arduino

##try:
mega = [arduino.Arduino('/dev/ttyACM0', b'?'), arduino.Arduino('/dev/ttyACM1', b'?'), arduino.Arduino('/dev/ttyACM2', b'?'), arduino.Arduino('/dev/ttyACM3', b'?')]
##finally:
    ##print('Unable to connect.\n')
    ##exit()

print('Connected!\n')
for i in mega:
    print(i.connect())
    i.getChanCount()
    i.reset()


while True:
    try:
        try:
            board = int(input("\nChoose Board (0 - 3): "))
            channel = int(input("Choose Channel (1 - %i): " % mega[board].chanCount))
            intensity = int(input("Select Intensity (0 - 255): "))

            if mega[board].setChannel(channel, intensity):
                print("Success!")
            else:
                print("Success not guaranteed.")
        except ValueError:
            print("Try again.")
            continue

        for i in mega:
            for j in i.getData():
                print(j)

    except KeyboardInterrupt:
        print('\n')
        exit()
