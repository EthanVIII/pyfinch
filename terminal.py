from lexome import translate_to_str


def main() -> None:
    runInterface()

def run_sim() -> None:
    str_orgs, str_lexome = list[list[str]],list[str]
    str_orgs, str_lexome = preprocessor.pre_process()

    binary_dict: dict = lexome.to_dict(str_lexome)
    str_dict: dict = dict(zip(binary_dict.values(),binary_dict.keys())) 

    binary_orgs: list[bytearray] = []
    for o in str_orgs:
        binary_orgs.append(lexome.translate_to_binary(o,binary_dict))
        print(binary_orgs[0])

    for o in binary_orgs:
        print(translate_to_str(o,str_dict))
        
    quit()

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
    import lexome
    main()