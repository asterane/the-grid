import select
import socket

import arduino
import cube

HOST = '10.101.50.102'  # Standard loopback interface address (localhost)
PORT = 2560             # Port to listen on (non-privileged ports are > 1023)

mega = [arduino.Arduino('/dev/ttyACM0', b'?'), arduino.Arduino('/dev/ttyACM1', b'?'),
        arduino.Arduino('/dev/ttyACM2', b'?'), arduino.Arduino('/dev/ttyACM3', b'?')]
for i in mega:
    i.connect()
    i.getChanCount()
    i.reset()

print('Connected to Arduinos!\n')

modes = {
    'S': "send",
    'Q': "quer",
    'C': "conn"}

endChar = 'Z'

currentMode = ""

mapping = [(3,32,30,36), (3,26,28,38), (3,42,1,23), (3,6,25,10), (3,41,31,29),
           (1,36,40,42), (1,34,32,30), (1,28,29,21), (1,22,13,8), (1,1,14,2),
           (3,3,21,34), (3,14,24,13), (3,15,2,4), (3,5,12,11), (3,35,37,27),
           (1,37,38,33), (1,25,24,45), (1,15,16,17), (1,3,12,4), (1,20,19,18),
           (3,22,44,45), (3,40,19,20), (3,17,18,16), (3,9,7,8), (3,43,39,33),
           (1,27,35,26), (1,41,31,39), (1,43,44,23), (1,10,5,6), (1,9,11,7),
           (2,34,32,31), (2,27,26,25), (2,10,13,15), (2,6,2,3), (2,24,11,12),
           (0,36,32,42), (0,40,34,38), (0,44,8,23), (0,3,4,13), (0,7,9,2),
           (2,29,28,30), (2,1,42,41), (2,18,20,21), (2,9,8,7), (2,4,44,5),
           (0,33,31,27), (0,30,28,26), (0,18,19,20), (0,1,25,10), (0,12,17,15),
           (2,37,40,38), (2,35,17,36), (2,22,23,43), (2,19,14,39), (2,33,45,16),
           (0,41,24,45), (0,29,43,22), (0,37,35,39), (0,21,11,6), (0,5,14,16)]

cubes = []

for i in range(len(mapping)):
    cubes.append(cube.Cube(mega[mapping[i][0]], mapping[i][1], mapping[i][2], mapping[i][3]))

def findMode(array):
    for i, b in enumerate(array):
        if chr(b) in modes.keys():
            mode = modes[chr(b)]
            return i, mode

def findEnd(array):
    for i, b in enumerate(array):
        if chr(b) == endChar:
            return i

buffer = bytearray()
chunk = bytearray()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    readable = [s]

    while True:
        openSocket,_,_ = select.select(readable,[],[],0.01)
        for sock in openSocket:
            if sock is s:
                conn, addr = sock.accept()
                print('Connected', addr)
                readable.append(conn)
            else:
                data = sock.recv(1024)
                if not data:
                    continue
                else:
                    buffer.extend(data)

        try:
            try:
                begin, currentMode = findMode(buffer)
                end = findEnd(buffer)

                chunk = buffer[begin+1:end]
                del buffer[0:end+1]
            except:
                pass

            if currentMode == "send":
                for i in range(0, len(chunk), 4):
                    cube = chunk[i]
                    newR = chunk[i+1]
                    newG = chunk[i+2]
                    newB = chunk[i+3]

                    print("\nCube:", cube)
                    print("R:", newR, "  G:", newG, "  B:", newB)
                    selection = cubes[cube]
                    #if selection.R != newR or selection.G != newG or selection.B != newB:
                    selection.setColor(newR, newG, newB)
                    selection.sendColor()
                del chunk[:]
            elif currentMode == "quer":
                pass
            elif currentMode == "conn":
                pass
            else:
                pass
        except:
            pass
