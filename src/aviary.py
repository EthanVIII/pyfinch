from finch import Finch
from visual import pretty
from lexome import *

def run_aviary(binary_lexome: list[bytearray], org_pops: list[int],binary_inst: bytearray, binary_dict: dict, str_dict: dict, size: int) -> None:
    # binary_dict   Key:lexemes Val:binary
    # str_dict      Key:binary  Val:lexemes

    finches: list[Finch] = []
    # Load finches
    for index, l in enumerate(binary_lexome):
        for i in range(org_pops[index]):
            finches.append(Finch(l))

    pretty("INFO","Innoculated aviary with starter finches")

    for i in range(1000):
        for finch in finches:
            if finch.skip_next_op:
                finch.inc()
                finch.skip_next_op = False
            else:
                run_op(str_dict,finch)

def ind_typecheck(var, expected_type) -> bool:
    if type(ind_typecheck) == expected_type:
        return True
    return False

def replication_queue() -> None:
    pass

def mutation() -> None:
    pass