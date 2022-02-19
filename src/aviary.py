from finch import Finch
from lexome import *

def run_aviary(
    binary_lexome: list[bytearray], 
    org_pops: list[int],binary_inst: bytearray, 
    binary_dict: dict, str_dict: dict, size: int) -> None:
    # binary_dict   Key:lexemes Val:binary
    # str_dict      Key:binary  Val:lexemes
    finches: list[Finch] = []
    unborn: list[Finch] = []
    # Load finches
    for index, l in enumerate(binary_lexome):
        for i in range(org_pops[index]):
            finches.append(Finch(l))
    pretty("INFO","Innoculated with starting Pop")
    pretty("INFO","Running Simulation...")
    for i in range(10):
        for finch in finches:
            
            run_op(str_dict,finch)
            if finch.init_divide:
                init_divide(finch, finches, unborn)
            finch.age += 1
        print("Pop: {}".format(str(len(finches))))
        replication_queue(finches, unborn)
        unborn = []
    pretty("INFO","Completed Simulation")

def init_divide(finch: Finch, finches: list[Finch], unborn: list[Finch]) -> None:
    pass

def replication_queue(finches: list[Finch], unborn: list[Finch]) -> None:
    pass

