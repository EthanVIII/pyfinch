class Finch:
    def __init__(self,lexome: bytearray):
        self.lexome = lexome
        self.ax: bytearray = (0).to_bytes(4,'big')
        self.bx: bytearray = (0).to_bytes(4,'big')
        self.cx: bytearray = (0).to_bytes(4,'big')
        self.s1: list[bytearray] = []
        self.s2: list[bytearray] = []
        self.read_h: int = 0
        self.writ_h: int = 0
        self.flow_h: int = 0 
        self.inst_h: int = 0
        self.input: list[bytearray] = [(0).to_bytes(4,'big'),(0).to_bytes(4,'big'),(0).to_bytes(4,'big')]
        self.output: bytearray - (0).to_bytes(4,'big')

    def mut(self, index: int, replacement: int):
        self.lexome[index] = replacement