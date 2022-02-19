from nbformat import read
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
    for i in range(1000):
        print("Pop: {}".format(str(len(finches))))
        for finch in finches:
            run_op(str_dict,finch)
            if finch.init_divide:
                init_divide(finch, unborn)
                finch.init_divide = False
            finch.age += 1
        replication_queue(finches, unborn)
        unborn = []
    pretty("INFO","Completed Simulation")

def init_divide(finch: Finch, unborn: list[Finch]) -> None:
    new_org_lexome: bytearray = finch.lexome[finch.read_h:tinc(finch.writ_h,len(finch.lexome))]
    new_org: Finch = Finch(new_org_lexome)
    finch.lexome = finch.lexome[:finch.read_h]
    if finch.inst_h > len(finch.lexome):
        finch.inst_h = 0
    finch.read_h = len(finch.lexome) - 1
    finch.writ_h = len(finch.lexome) - 1
    if finch.flow_h > len(finch.lexome):
        finch.flow_h = len(finch.lexome) - 1
    unborn.append(new_org)

def replication_queue(finches: list[Finch], unborn: list[Finch]) -> None:
    for f in unborn:
        finches.append(f)

