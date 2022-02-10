class Finch:
    def __init__(self,lexome: bytearray) -> None:
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

    def __str__(self) -> str:
        buffer: list[str] = []
        buffer.append("-----\n")
        buffer.append("aX: ")
        buffer.append(str(int.from_bytes(self.ax,'big')))
        buffer.append(" bX: ")
        buffer.append(str(int.from_bytes(self.bx,'big')))
        buffer.append(" cX: ")
        buffer.append(str(int.from_bytes(self.cx,'big')))
        buffer.append("\n")
        buffer.append("Stack 1: ")
        buffer.append(str(self.s1))
        buffer.append("\n")
        buffer.append("Stack 2: ")
        buffer.append(str(self.s2))
        buffer.append("\n")
        buffer.append("-----")
        return "".join(buffer)
