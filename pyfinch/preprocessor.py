from .visual import pretty


def pre_process() -> tuple[list[list[str]], list[int], list[str], int]:
    lexome_name = ""
    orgs = []

    # Parses Config File Once and all at once.
    org_names, org_pops, lexome_name, size = finch_parser("default")
    pretty("INFO", "Parsed PYFINCH config")

    # Parses Lexome Set
    try:
        f = open("lexome\{}.cfg".format(lexome_name), "r", encoding="utf-8")
    except:
        pretty("PANIC", "{}.cfg was not found in lexome folder".format(lexome_name))
    lines = f.readlines()
    f.close()
    lexome = lexome_parser(lines)
    pretty("INFO", "Parsed lexome sets")

    # Parses Organism - Checks lexome for errors.
    for org_name in org_names:
        try:
            f = open("org\{}.lxm".format(org_name), "r", encoding="utf-8")
        except:
            pretty(
                "PANIC",
                "Specified organism lexome ({}.lxm) was not found in org folder".format(
                    org_name
                ),
            )
        lines = f.readlines()
        f.close()
        temp_org = org_parser(lines)
        if len(temp_org) == 0:
            pretty(
                "WARNING", "There is no lexome for this organism ({})".format(org_name)
            )
        result, offending = org_check(lexome, temp_org)
        if not result:
            pretty(
                "PANIC",
                "The lexome for this organism ({}) contains Ops that are not a part of the Lexome Set ({})".format(
                    org_name, offending
                ),
            )
        orgs.append(temp_org)
    pretty("INFO", "Parsed organism lexomes")
    return (orgs, org_pops, lexome, size)


# Validates that organism org complies to the instruction set lexome_set
def org_check(lexome_set: list[str], org: list[str]) -> tuple[bool, str | None]:
    for x in org:
        if x not in lexome_set:
            return (False, x)
    return (True, None)


# Parses organism from lexome file (list of strings)
def org_parser(ops: list[str]) -> list[str]:
    org_intermediary: list[str] = []
    for o in ops:
        o_split = o.split("#")
        first_str = o_split[0].strip()
        if first_str == "":
            continue
        org_intermediary.append(first_str)
    return org_intermediary


# Parses lexome from file
def lexome_parser(ops: list[str]) -> list[str]:
    o_split: list[str] = []
    lexome_intermediary: list[str] = []
    for o in ops:
        o_split += o.split(" ")
    o_split = list(map(str.strip, filter(lambda x: x != "\n", o_split)))
    for index, o in enumerate(o_split):
        is_last = (index + 1) == len(o_split)
        if o == "INST":
            if is_last:
                pretty(
                    "PANIC",
                    "Lexome config was formatted incorrectly. There are tailing tags present.",
                )
            if o_split[index + 1] == "INST":
                pretty(
                    "PANIC",
                    "Lexome config was formatted incorrectly. There are back-to-back INST.",
                )
            lexome_intermediary.append(o_split[index + 1])
    return lexome_intermediary


# Parses and checks config file. File has to be in a subfolder config\default.cfg.
def finch_parser(name: str) -> tuple[list[str], list[int], str, int]:
    try:
        with open("config\{}.cfg".format(name), "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        pretty("PANIC", "Finch config was not found in config subfolder.")
    org_names = []
    lexome_name = ""
    org_pops: list[int] = []
    size = -1
    for row, line in enumerate(lines):
        entry = line.split(" ")
        if len(entry) == 1 and entry[0] != "\n":
            pretty(
                "PANIC",
                "Finch Config was formatted incorrectly. Blank fields were found.",
            )

        en0 = entry[0]
        if en0 == "\n":
            pass
        elif en0 == "#":
            pass
        elif en0 == "LEXOME":
            lexome_name = entry[1].strip()
        elif en0 == "SIZE":
            size = int(entry[1].strip())
        elif en0 == "ORG":
            org_names = list(map(str.strip, entry[1::2]))
            org_pops = list(map(int, list(map(str.strip, entry[2::2]))))
        else:
            pretty(
                "PANIC",
                "Finch Config contains unknown command in line {} and command {}".format(
                    row, entry[0]
                ),
            )

    if size == -1:
        pretty("PANIC", "Finch Config did not specify a valid aviary size.")
    return (org_names, org_pops, lexome_name, size)
