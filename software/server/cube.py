import arduino


class Cube:
    def __init__(self, board: arduino.Arduino, *channels):
        self.board = board
        self.channels = channels

        self.chanR, self.chanG, self.chanB = channels
        self.R, self.G, self.B = 0, 0, 0

    def setColor(self, red, green, blue):
        self.R = red
        self.G = green
        self.B = blue

    def sendColor(self):
        self.board.setChannel(self.chanR, self.R, False)
        self.board.setChannel(self.chanG, self.G, False)
        self.board.setChannel(self.chanB, self.B, False)
