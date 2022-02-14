import copy

from .finch import Finch
from .visual import pretty


def run_op(str_dict: dict, finch: Finch) -> str:
    op: str = str_dict[finch.lexome[finch.inst_h].to_bytes(1, "big")]
    exec(op + "(finch,str_dict)")
    return op


def tinc(current: int, length: int, step=1) -> int:
    if current + step >= length:
        return current + step - length
    if current >= length:
        pretty(
            "WARNING",
            "function tinc() in lexome.py has incremented a pointer > lexome.",
        )
    return current + step


# Calculates the complement of the a-b-c label
def comp(register: int) -> int:
    if register == 2:
        return 0
    return register + 1


def next_nop(finch: Finch, str_dict: dict) -> int:
    next_str: str = str_dict[
        finch.lexome[tinc(finch.inst_h, len(finch.lexome))].to_bytes(1, "big")
    ]
    if next_str == "nop_A":
        return 0
    elif next_str == "nop_B":
        return 1
    elif next_str == "nop_C":
        return 2
    else:
        return 3


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
    else:
        finch.skip_next_op = False
    finch.inc()


def if_less(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    if finch.register[reg] >= finch.register[comp(reg)]:
        finch.skip_next_op = True
    else:
        finch.skip_next_op = False
    finch.inc()


def pop(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    element: bytearray = bytearray((0).to_bytes(4, "big"))
    if finch.stacks[finch.active] != []:
        element = finch.stacks[finch.active][-1]
    finch.register[reg] = element
    finch.inc()


def push(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
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
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg], finch.register[comp(reg)] = (
        finch.register[comp(reg)],
        finch.register[reg],
    )
    finch.inc()


def shift_r(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (int.from_bytes(finch.register[reg], "big") >> 1).to_bytes(4, "big")
    )
    finch.inc()


def shift_l(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (int.from_bytes(finch.register[reg], "big") << 1).to_bytes(4, "big")
    )
    finch.inc()


def inc(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (int.from_bytes(finch.register[reg], "big") + 1).to_bytes(4, "big")
    )
    finch.inc()


def dec(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (int.from_bytes(finch.register[reg], "big") - 1).to_bytes(4, "big")
    )
    finch.inc()


def add(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        int.from_bytes(finch.register[1], "big")
        + int.from_bytes(finch.register[2], "big")
    )
    finch.inc()


def sub(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (
            int.from_bytes(finch.register[1], "big")
            - int.from_bytes(finch.register[2], "big")
        ).to_bytes(4, "big")
    )
    finch.inc()


def xor(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.register[reg] = bytearray(
        (
            int.from_bytes(finch.register[1], "big")
            ^ int.from_bytes(finch.register[2], "big")
        ).to_bytes(4, "big")
    )
    finch.inc()


def io(finch: Finch, str_dict: dict) -> None:
    # ?BX?
    reg: int = next_nop(finch, str_dict)
    if reg == 3:
        reg = 1
    finch.output = copy.copy(finch.register[reg])
    finch.register[reg] = copy.copy(finch.input[0])
    finch.inc()


def mov_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch, str_dict)
    if head == 3:
        head = 0

    if head == 0:
        finch.inst_h = copy.copy(finch.flow_h)
    elif head == 1:
        finch.read_h = copy.copy(finch.flow_h)
    elif head == 2:
        finch.writ_h = copy.copy(finch.flow_h)

    # XXX: What if head > 2?

    finch.inc()


def jmp_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch, str_dict)
    if head == 3:
        head = 0

    if head == 0:
        finch.inst_h = tinc(finch.inst_h, len(finch.lexome), finch.register[2])
    elif head == 1:
        finch.read_h = tinc(finch.read_h, len(finch.lexome), finch.register[2])
    elif head == 2:
        finch.writ_h = tinc(finch.read_h, len(finch.lexome), finch.register[2])

    # XXX: What if head > 2?

    finch.inc()


def get_head(finch: Finch, str_dict: dict) -> None:
    # ?IP?
    head: int = next_nop(finch, str_dict)
    if head == 3:
        head = 0

    if head == 0:
        finch.register[2] = bytearray(finch.inst_h.to_bytes(4, "big"))
    elif head == 1:
        finch.register[2] = bytearray(finch.read_h.to_bytes(4, "big"))
    elif head == 2:
        finch.register[2] = bytearray(finch.writ_h.to_bytes(4, "big"))

    # XXX: What if head > 2?

    finch.inc()


def h_alloc(finch: Finch, str_dict: dict) -> None:
    print("h_alloc - unimplemented")


def h_divide(finch: Finch, str_dict: dict) -> None:
    print("h_divide - unimplemented")


def h_copy(finch: Finch, str_dict: dict) -> None:
    print("h_copy - unimplemented")


def h_search(finch: Finch, str_dict: dict) -> None:
    print("h_search - unimplemented")


def if_label(finch: Finch, str_dict: dict) -> None:
    print("if_label - unimplemented")


def set_flow(finch: Finch, str_dict: dict) -> None:
    print("set_flow - unimplemented")
