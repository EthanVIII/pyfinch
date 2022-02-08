from finch import Finch
from visual import pretty
def run_aviary(binary_lexome: list[bytearray], org_pops: list[int],binary_inst: bytearray, binary_dict: dict, str_dict: dict, size: int):
    # binary_dict   Key:lexemes Val:binary
    # str_dict      Key:binary  Val:lexemes

    finches: list[Finch] = []
    # Load finches
    for index, l in enumerate(binary_lexome):
        for i in range(org_pops[index]):
            finches.append(Finch(l))
    
    pretty("INFO","Innoculated aviary with starter finches")

    for i in range(1000):
        pass

def mutation():
    pass