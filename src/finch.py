class Finch:
    def __init__(self,lexome: bytearray) -> None:
        i32_BA: bytearray = bytearray((0).to_bytes(4,'big'))
        self.lexome = lexome
        self.ax: bytearray = i32_BA.copy()
        self.bx: bytearray = i32_BA.copy()
        self.cx: bytearray = i32_BA.copy()
        self.s1: list[bytearray] = []
        self.s2: list[bytearray] = []
        self.read_h: int = 0
        self.writ_h: int = 0
        self.flow_h: int = 0 
        self.inst_h: int = 0
        self.input: list[bytearray] = [i32_BA.copy() for i in range(3)]
        self.output: bytearray = i32_BA.copy()
        del i32_BA

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
