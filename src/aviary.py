from sys import stdout
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
    index: int = 0
    while True:
        if index % 100 == 0:
            print("Gen: {} Pop: {}".format(index,str(len(finches))))
        for finch in finches:
            # if i == 10:
            #     print(finch)
            run_op(str_dict,finch)
            if finch.init_divide:
                init_divide(finch, unborn)
                finch.init_divide = False
            finch.age += 1
        for f in unborn:
            finches.append(f)
        unborn = []
        index += 1
    pretty("INFO","Completed Simulation")

def init_divide(finch: Finch, unborn: list[Finch]) -> None:
    new_org_lexome: bytearray = finch.lexome[finch.read_h:finch.writ_h]
    new_org: Finch = Finch(new_org_lexome)
    finch.lexome = finch.lexome[:finch.read_h]
    if finch.inst_h > len(finch.lexome):
        finch.inst_h = len(finch.lexome)-1
    if finch.flow_h > len(finch.lexome):
        finch.flow_h = len(finch.lexome) - 1
    finch.inc()
    unborn.append(new_org)
    finch.read_h = finch.writ_h = finch.inst_h = 0


