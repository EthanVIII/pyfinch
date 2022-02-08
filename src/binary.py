from visual import pretty


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
    pretty("INFO","Validated INST set")
    return ret_dict



    
