import socket

HOST = '10.101.50.102'  # The server's hostname or IP address
PORT = 2560             # The port used by the server

buffer = bytearray()

def openSocket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def closeSocket(s):
    s.shutdown(socket.SHUT_RDWR)
    s.close()

def sendColor(s, X, Y, R, G, B, len):
    packet = bytearray()
    packet.append(ord('S'))

    for i in range(len):
        cube = (10 * X[i]) + Y[i]
        packet.extend([int(cube), int(R[i]), int(G[i]), int(B[i])])

    packet.append(ord('Z'))
    print("\nSending")
    print(packet)
    s.sendall(packet)
