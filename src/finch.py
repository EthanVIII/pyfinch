class Finch:
    lexome: bytearray = bytearray()
    lexeme_step: int = 0

    def __init__(self,lexome: bytearray):
        self.lexome = lexome
        self.lexeme_step = 0
    
    def inc(self):
        if self.lexeme_step < len(self.lexome)-1:
            self.lexeme_step = 0
        else:
            self.lexeme_step += 1

    def mut(self, index: int, replacement: int):
        self.lexome[index] = replacement