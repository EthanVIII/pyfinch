def main() -> None:
    os.chdir("..")
    runInterface()

# Option to run the simulation
def run_sim() -> None:
    pretty("SPRT", "Starting Pre-Processing & Parsing (IO)")
    str_orgs: list[list[str]] = [[]]
    str_lexome: list[str] = []
    size: int = 0
    org_pops: list[int] = []
    str_orgs,org_pops, str_lexome, size = preprocessor.pre_process()

    # Converts lexemes to binary
    binary_dict: dict = bytedict.to_dict(str_lexome)
    # Converts binary to lexemes
    str_dict: dict = dict(zip(binary_dict.values(),binary_dict.keys())) 

    pretty("SPRT","Completed Pre-Processing & Parsing (IO)")


    binary_orgs: list[bytearray] = []
    # Binary Lexome - will be used for mutation
    binary_lexome: bytearray = bytedict.translate_to_bytes(str_lexome,binary_dict)

    # Read string organisms and translate to binary.
    for o in str_orgs:
        binary_orgs.append(bytedict.translate_to_bytes(o,binary_dict))

    print()
    pretty("SPRT", "Loading up aviary for finches")
    aviary.run_aviary(binary_orgs,org_pops, binary_lexome, binary_dict, str_dict, size)

    quit()

# Startup interface
def runInterface() -> None:
    buffer: str = ""
    title_buffer: str =  "-"*23 + "\n"
    title_buffer +=      "PYFINCH - ALPHA BUILD\n"
    title_buffer +=      "-"*23
    for i, (option,_) in enumerate(optionHandler(get=True)):
        buffer += "[" + str(i) +  "]: " + option + "\n"
    while True:
        pretty("HEADER",title_buffer)
        pretty("BOLD",buffer)
        action: list[(str,str)] = optionHandler(input())
        if action[0][0] == "NOP":
            print("Invalid Action")
        else:
            exec(action[1])

# Handles the display menus - easily updateable.
def optionHandler(option: str = None, get: bool=False) -> list[(str,str)]:
    options: list[(str,str)] = []
    options.append(("Run Simulation - Run a preset simulation","run_sim()"))
    options.append(("About - Information about PYFINCH","about()"))
    options.append(("Quit - Quit PYFINCH","quit()"))
    if get:
        return options
    try:
        choice: int = int(option)
    except:
        return [("NOP","NOP")]
    if choice >= len(options) or choice < 0:
        return [("NOP","NOP")]
    return options[choice]

# Option to display About.
def about() -> None:
    try:
        with open("about.txt",'r',encoding='utf-8') as f:
            lines = f.read()
        print(lines)
    except:
        pretty("WARNING","The file (about.txt) could not be found in top level directory")

if __name__ == "__main__":
    import preprocessor
    from visual import pretty
    import aviary
    import bytedict
    import os
    main()