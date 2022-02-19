from numpy import byte
from finch import Finch
from visual import pretty
import copy

def run_op(str_dict: dict, finch: Finch) -> str:
    op: str = str_dict[finch.lexome[finch.inst_h].to_bytes(1,'big')]
    if finch.skip_next_op:
        if all(op != x for x in ('nop_A','nop_B','nop_C')):
            finch.inc()
            finch.skip_next_op = False
            return op
    exec(op +"(finch,str_dict)")
    return op

def mutation(op) -> int:
    return op

# Theoretically increment a pointer on a looped array.
# Calculates outcome.
def tinc(current: int, length: int, step=1) -> int:
    if current+step >= length:
        return current + step - length
    if current >= length:
        pretty("WARNING","function tinc() in lexome.py has incremented a pointer > lexome.")
    return current+step

# Calculates the complement of the a-b-c label
def comp(register: int) -> int:
    if register == 2:
        return 0 
    return register + 1


# Returns the next nop if there is one. otherwise returns 3.
def next_nop(finch: Finch, str_dict: dict) -> int:
    next_str: str = str_dict[finch.lexome[tinc(finch.inst_h, len(finch.lexome))].to_bytes(1,'big')]
    if next_str == "nop_A":
        return 0
    elif next_str == "nop_B":
        return 1
    elif next_str == "nop_C":
        return 2
    return 3

# Returns the next list of complement nops if there is one, otherwise returns blank bytearray.
def next_comp_nop_list(finch: Finch, str_dict: dict) -> tuple[list[int],int]:
    ret_register: list[int] = []
    ptr: int = tinc(finch.inst_h, len(finch.lexome))
    # Bad practice lmao ik dw.
    while True:
        if str_dict[finch.lexome[ptr]] == 'nop_A':
            ret_register.append(1)
        elif str_dict[finch.lexome[ptr]] == 'nop_B':
            ret_register.append(2)
        elif str_dict[finch.lexome[ptr]] == 'nop_C':
            ret_register.append(0)
        else: break
        ptr = tinc(ptr,len(finch.lexome))
    
    # ptr is now length of nop.
    if ptr > finch.inst_h:
        ptr = ptr - finch.inst_h - 1
    else:
        ptr = (len(finch.lexome) - finch.inst_h - 1) + (ptr - 1)
    return (ret_register, ptr)

#---------------------- CPU Operations ----------------------#

# Instruction No-Ops
def nop_B(finch: Finch, str_dict: dict) -> None:
    finch.inc()
def nop_A(finch: Finch, str_dict: dict) -> None:
    finch.inc()
def nop_C(finch: Finch, str_dict: dict) -> None:
    finch.inc()

def if_n_equ(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    if finch.register[reg] == finch.register[comp(reg)]:
        finch.skip_next_op = True
    finch.inc()

def if_less(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    if finch.register[reg] >= finch.register[comp(reg)]:
        finch.skip_next_op = True
    finch.inc()

def pop(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    element: bytearray = bytearray((0).to_bytes(4,'big'))
    if finch.stacks[finch.active] != []:
        element = finch.stacks[finch.active][-1]
    finch.register[reg] = element
    finch.inc()

def push(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.stacks[finch.active].append(finch.register[reg])
    finch.inc()

def swap_stk(finch: Finch, str_dict: dict) -> None:
    if finch.active == 0:
        finch.active = 1
    else:
        finch.active = 0
    finch.inc()

def swap(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg], finch.register[comp(reg)] = finch.register[comp(reg)], finch.register[reg]
    finch.inc()

def shift_r(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray((int.from_bytes(finch.register[reg],'big') >> 1).to_bytes(4,'big'))
    finch.inc()

def shift_l(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray((int.from_bytes(finch.register[reg],'big') << 1).to_bytes(4,'big'))
    finch.inc()

def inc(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg]  = bytearray((int.from_bytes(finch.register[reg],'big') + 1).to_bytes(4,'big'))
    finch.inc()

def dec(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg]  = bytearray((int.from_bytes(finch.register[reg],'big') - 1).to_bytes(4,'big'))
    finch.inc()

def add(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(int.from_bytes(finch.register[1],'big') + int.from_bytes(finch.register[2],'big'))
    finch.inc()

def sub(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1 
    finch.register[reg] = bytearray((int.from_bytes(finch.register[1],'big') - int.from_bytes(finch.register[2],'big')).to_bytes(4,'big'))
    finch.inc()

def xor(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1 
    finch.register[reg] = bytearray((int.from_bytes(finch.register[1],'big') ^ int.from_bytes(finch.register[2],'big')).to_bytes(4,'big'))
    finch.inc()

def io(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 1
    finch.output = copy.copy(finch.register[reg])
    finch.register[reg] = copy.copy(finch.input[0])
    finch.inc()

def mov_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch,str_dict)
    if head == 3:
        head = 0
    if head == 0:
        finch.inst_h = copy.copy(finch.flow_h)
    elif head == 1:
        finch.read_h = copy.copy(finch.flow_h)
        finch.inc()
    elif head == 2:
        finch.writ_h = copy.copy(finch.flow_h)
        finch.inc()

def jmp_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch,str_dict)
    if head == 3:
        head = 0
    if head == 0:
        finch.inst_h = tinc(finch.inst_h,len(finch.lexome),finch.register[2])
    elif head == 1:
        finch.read_h = tinc(finch.read_h,len(finch.lexome),finch.register[2])
        finch.inc()
    elif head == 2:
        finch.writ_h = tinc(finch.read_h,len(finch.lexome),finch.register[2])
        finch.inc()

def get_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch,str_dict)
    if head == 3:
        head = 0
    if head == 0:
        finch.register[2] = bytearray(finch.inst_h.to_bytes(4,'big'))
    elif head == 1:
        finch.register[2] = bytearray(finch.read_h.to_bytes(4,'big'))
    elif head == 2:
        finch.register[2] = bytearray(finch.writ_h.to_bytes(4,'big'))
    finch.inc()
    
# Allocates the maximum length for offspring replication.
# Currently is set to the length of the ori org.
def h_alloc(finch: Finch, str_dict: dict) -> None:
    finch.register[0] = bytearray(len(finch.lexome))
    finch.lexome.append(len(finch.lexome))
    finch.inc()
    
# Special Command that needs to happen by the aviary controller.
# IP will be incremented then too.
def h_divide(finch: Finch, str_dict: dict) -> None:
    finch.init_divide = True
    print("h_divide - unimplemented")

def h_copy(finch: Finch, str_dict: dict) -> None:
    copy_elem: int = mutation(copy.copy(finch.lexome[finch.read_h]))
    finch.copy_buffer.append(copy_elem)
    finch.lexome[finch.writ_h] = copy_elem
    finch.inc()

def h_search(finch: Finch, str_dict: dict) -> None:
    # Extract next nops next_comp_nop_list(finch: Finch, str_dict: dict) -> tuple[list[int],int]
    next_nops: tuple[list[int],int] = next_comp_nop_list(finch,str_dict)
    if next_nops[0] == []:
        finch.register[1] = bytearray((0).to_bytes(1,'big'))
        finch.register[2] = bytearray((0).to_bytes(1,'big'))
        finch.flow_h = tinc(finch.inst_h,len(finch.lexome))
        return

    # preprocess lexome
    lexome_copy: bytearray = bytearray(finch.lexome[finch.inst_h:] + finch.lexome[:finch.inst_h])
    temp_holder: list[int] = []
    ptr_list: list[int] = []
    is_added: bool = False
    check_list: list[list[int]] = []
    pos: int = finch.inst_h
    for b in lexome_copy:
        if str_dict[b.to_bytes(1,'big')] == 'nop_A':
            if not is_added: 
                ptr_list.append(pos)
                is_added = True
            temp_holder.append(1)
        elif str_dict[b.to_bytes(1,'big')] == 'nop_B':
            if not is_added: 
                ptr_list.append(pos)
                is_added = True
            temp_holder.append(2)
        elif str_dict[b.to_bytes(1,'big')] == 'nop_C':
            if not is_added: 
                ptr_list.append(pos)
                is_added = True            
            temp_holder.append(0)
        elif temp_holder != []:
            check_list.append(temp_holder)
            is_added = False
            temp_holder = []
        pos = tinc(pos, len(finch.lexome))
    
    for index, c in enumerate(check_list):
        if next_nops[0] == c:
            finch.flow_h = ptr_list[index]
            finch.register[2] = bytearray(next_nops[1].to_bytes(1,'big'))
            if finch.flow_h >= finch.inst_h:
                finch.register[1] = bytearray((finch.flow_h - finch.inst_h).to_bytes(1,'big'))
            else:
                finch.register[1] = bytearray(((len(finch.lexome) - finch.inst_h) + finch.flow_h + 1).to_bytes(1,'big'))
            return
            
    finch.register[1] = bytearray((0).to_bytes(1,'big'))
    finch.register[2] = bytearray((0).to_bytes(1,'big'))
    finch.flow_h = tinc(finch.inst_h,len(finch.lexome))


# Toss up on if there is no label what the behaviour is.
def if_label(finch: Finch, str_dict: dict) -> None:
    next_nops: tuple[list[int],int] = next_comp_nop_list(finch, str_dict)
    if next_nops[0] != []:
        for index, op in enumerate(finch.copy_buffer[-next_nops[1]:]):
            if str_dict[op] != next_nops[0][index]:
                finch.inc()
                return
        finch.skip_next_op = True
    finch.inc()

def set_flow(finch: Finch, str_dict: dict) -> None:
    # ?CX?
    reg: int = next_nop(finch,str_dict)
    if reg == 3:
        reg = 2
    if int.from_bytes(finch.register[reg],'big') < len(finch.lexome) and int.from_bytes(finch.register[reg],'big') >= 0:
        finch.flow_h = int.from_bytes(finch.register[reg],'big')
    finch.inc()