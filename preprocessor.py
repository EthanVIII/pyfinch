from visual import pretty

def pre_process() -> bool:
    parsed = bool
    org_names, lexomes_names = list[str], list[str]
    orgs, lexomes = list[list[str]],list[list[str]]
    orgs, lexomes = [], []

    # Parses Config File Once and all at once.
    org_names, lexomes_names = finch_parser("default")
    pretty("INFO","Parsed PYFINCH config")
    
    # Parses Lexome Set
    for lexome_name in lexomes_names:
        try:
            f = open("lexome\{}.cfg".format(lexome_name),'r',encoding="utf-8") 
        except:
            pretty("PANIC","{} was not found in lexome folder".format(lexome_name))
        lines: list[str] = f.readlines()
        f.close()
        lexomes.append(lexome_parser(lines))
    pretty("INFO","Parsed lexome sets")

    # Parses Organism - Checks lexome for errors.
    for org_name in org_names:
        try: 
            f = open("org\{}.lxm".format(org_name),'r',encoding="utf-8")
        except:
            pretty("PANIC", "Specified organism lexome ({}.lxm) was not found in org folder".format(org_name))
        lines: list[str] = f.readlines()
        f.close()
        temp_org: list[str] = org_parser(lines)
        if len(temp_org) == 0:
            pretty("WARNING","There is no lexome for this organism ({})".format(org_name))
        if not org_check(lexomes[0],temp_org):
            pretty("PANIC","The lexome for this organism ({}) contains Ops that are not a part of the Lexome Set".format(org_name))
        orgs.append(temp_org)
    pretty("INFO", "Parsed organism lexomes")
    return True

def org_check(lexome_set: list[str],org: list[str]) -> bool:
    for x in org:
        if x not in lexome_set:
            return False
    return True

def org_parser(ops: list[str]) -> list[str]:
    o_split: list[str] = []
    org_intermediary: list[str] = []
    for o in ops:
        o_split = o.split("#")
        first_str: str = o_split[0].strip()
        if first_str == '':
            continue
        org_intermediary.append(first_str)
    return org_intermediary

# Parses lexome from file
# We will see if lexome needs to be presented as bytes or not.
def lexome_parser(ops: list[str]) -> list[str]:
    o_split: list[str] = []
    lexome_intermediary: list[str] = []
    for o in ops:
        o_split += o.split(" ")
    o_split = list(map(str.strip,filter(lambda x: x != "\n", o_split)))
    for index, o in enumerate(o_split):
        is_last: bool = (index+1) == len(o_split)
        if o == "INST":
            if is_last:
                pretty("PANIC", "Lexome config was formatted incorrectly. There are tailing tags present.")
            if o_split[index+1] == "INST":
                pretty("PANIC", "Lexome config was formatted incorrectly. There are back-to-back INST.")
            lexome_intermediary.append(o_split[index+1])
    return lexome_intermediary

# Parses and checks config file. File has to be in a subfolder config\default.finch.
# TODO implement changes for this method.
def finch_parser(name: str) -> tuple[list[str],list[str]]:
    try:
        with open("config\{}.finch".format(name),'r',encoding='utf-8') as f:
            lines: list[str] = f.readlines()
    except:
        pretty("PANIC", "Finch config was not found in config subfolder.")
    org_names: list[str] = []
    lexome_names: list[str] = []
    for row, line in enumerate(lines):       
        entry: list[str] = line.split(" ")
        if len(entry) == 1 and entry[0] != '\n':
            pretty("PANIC", "Finch Config was formatted incorrectly. Blank fields were found.")
        match (entry[0]):
            case "\n":
                pass
            case "#":
                pass
            case "LEXOME":
                lexome_names.append(entry[1].strip())
            #TODO Implement Size.
            case "SIZE":
                pass
            case "ORG":
                org_names.append(entry[1].strip())
            case _:
                pretty("PANIC","Finch Config contains unknown command in line {} and command {}".format(row,entry[0]))
    return (org_names,lexome_names)