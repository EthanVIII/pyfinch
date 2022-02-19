class Finch:
    def __init__(self,lexome: bytearray) -> None:
        # Components - CPU, Memory, Output
        i32_BA: bytearray = bytearray((0).to_bytes(4,'big'))
        self.lexome = lexome
        self.register: list[bytearray] = [i32_BA.copy() for i in range(3)]
        self.stacks: list[list[bytearray]] = [[],[]]
        self.active: int = 0
        self.s1: list[bytearray] = []
        self.s2: list[bytearray] = []
        self.read_h: int = 0
        self.writ_h: int = 0
        self.flow_h: int = 0 
        self.inst_h: int = 0
        self.input: list[bytearray] = [i32_BA.copy() for i in range(3)]
        self.output: bytearray = i32_BA.copy()
        
        # Attributes
        self.age: int = 0
        self.init_divide: bool = False
        self.skip_next_op: bool = False
        self.copy_buffer: bytearray = bytearray()

        # C
        del i32_BA
    
    # Increments the instruction head for the next cycle.
    # Lexome is a loop.
    def inc(self) -> None:
        if self.inst_h + 1 == len(self.lexome):
            self.inst_h = 0
        else:
            self.inst_h += 1

    # Mutates lexome with a particular replacement.
    def mut(self, index: int, replacement: int) -> None:
        self.lexome[index] = replacement

    # Print function.
    def __str__(self) -> str:
        buffer: list[str] = []
        buffer.append("-----\n")
        buffer.append("Age: {} Lexome Length: {}".format(self.age,len(self.lexome)))
        buffer.append("\naX: ")
        buffer.append(str(int.from_bytes(self.register[0],'big')))
        buffer.append(" bX: ")
        buffer.append(str(int.from_bytes(self.register[1],'big')))
        buffer.append(" cX: ")
        buffer.append(str(int.from_bytes(self.register[2],'big')))
        buffer.append("\n")
        buffer.append("Stack 1: ")
        buffer.append(str(self.stacks[0]))
        buffer.append("\n")
        buffer.append("Stack 2: ")
        buffer.append(str(self.stacks[1]))
        buffer.append("\n")
        buffer.append("IP: ")
        buffer.append(str(self.inst_h))
        buffer.append(" Flow: ")
        buffer.append(str(self.flow_h))
        buffer.append(" Read: ")
        buffer.append(str(self.read_h))
        buffer.append(" Write: ")
        buffer.append(str(self.writ_h))
        buffer.append("\n")
        buffer.append("-----")
        return "".join(buffer)
