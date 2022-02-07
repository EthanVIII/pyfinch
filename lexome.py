from preprocessor import finch_parser
from visual import pretty
from finch import Finch

### TESTING ###
def run_op(op: bytes, str_dict: dict, finch: Finch):
    exec(str(str_dict[op])+"(finch)")

def h_alloc(finch: Finch):
    print("h_alloc")

def h_search(finch: Finch):
    print("h_search")

def h_copy(finch: Finch):
    print("h_copy")

def if_label(finch: Finch):
    print("if_label")

def h_divide(finch: Finch):
    print("h_divide")

def nop_C(finch: Finch):
    print("nop_C")

def nop_A(finch: Finch):
    print("nop_A")

def nop_B(finch: Finch):
    print("nop_B")

def mov_head(finch: Finch):
    print("mov_head")
### TESTING

# Converts lexome set to binary dictionary.
# Also does some checking to ensure that instruction set is a subset of all master operations.
def to_dict(lexomes: list[str]) -> list[bytearray]:
    inc_int: int = 0
    master_lexome: list[str] = []
    lexome_clean: list[str] = list(set(lexomes))
    ret_dict: dict = dict()
    try:
        f = open("config\master_lexome.cfg",'r',encoding="utf-8")
    except:
        pretty("PANIC","master_lexome.cfg was not found in the config subfolder. Unable to parse master instruction set.")
    lines: list[str] = f.readlines()
    for l in lines:
        first_str: str = l.split("#")[0].strip()
        if first_str != "":
            master_lexome.append(first_str)

    for l in lexome_clean:
        if l not in master_lexome:
            pretty("PANIC", "Instruction set contains implemented operation ({}). Unable to parse master instruction set.".format(l))
        ret_dict[l] = inc_int.to_bytes(1,'big')
        inc_int += 1
    if len(lexomes) != len(lexome_clean):
        
        pretty("WARNING", "Instruction set contains duplicate instructions")
    pretty("INFO","Validated lexome sets")

    pretty("INFO","Loaded binary dictionary")
    return ret_dict

# Using a provided dictionary, translates a lexome to bytearrays.
def translate_to_binary(org: list[str],l_dict: dict) -> bytearray:
    ret_bytes: bytearray = bytearray()
    for o in org:
        ret_bytes.extend(l_dict[o])
    return ret_bytes

# Using a provided dictionary, translates a bytearray to lexome.
def translate_to_str(org: bytearray,l_dict: dict) -> list[str]:
    ret_list: list[str] = []
    for x in org:
        ret_list.append(l_dict[x.to_bytes(1,'big')])
    return ret_list



    
