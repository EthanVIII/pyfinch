from . import aviary, bytedict, preprocessor
from .visual import pretty

OPTIONS = [
    (0, "Run Simulation - Run a preset simulation", "run_sim()"),
    (1, "About - Information about PYFINCH", "about()"),
    (2, "Quit - Quit PYFINCH", "quit()"),
]


def main() -> None:
    # import os
    # os.chdir("..")
    runInterface()


# Option to run the simulation
def run_sim() -> None:
    pretty("SPRT", "Starting Pre-Processing & Parsing (IO)")
    str_orgs: list[list[str]] = [[]]
    str_lexome: list[str] = []
    size: int = 0
    org_pops: list[int] = []
    str_orgs, org_pops, str_lexome, size = preprocessor.pre_process()

    # Converts lexemes to binary
    binary_dict: dict = bytedict.to_dict(str_lexome)
    # Converts binary to lexemes
    str_dict: dict = dict(zip(binary_dict.values(), binary_dict.keys()))

    pretty("SPRT", "Completed Pre-Processing & Parsing (IO)")

    binary_orgs: list[bytearray] = []
    # Binary Lexome - will be used for mutation
    binary_lexome: bytearray = bytedict.translate_to_bytes(str_lexome, binary_dict)

    # Read string organisms and translate to binary.
    for o in str_orgs:
        binary_orgs.append(bytedict.translate_to_bytes(o, binary_dict))

    print()
    aviary.run_aviary(binary_orgs, org_pops, binary_lexome, binary_dict, str_dict, size)

    quit()


# Startup interface
def runInterface() -> None:
    buffer: str = ""
    title_buffer: str = "-" * 23 + "\n"
    title_buffer += "PYFINCH - ALPHA BUILD\n"
    title_buffer += "-" * 23

    # Alternatively, using `list comprehension`
    #   buffer = '\n'.join(
    #                   f"[{i}] {option}" for (i, option, _) in OPTIONS
    #                   )
    for i, option, _ in OPTIONS:
        buffer += f"[{i}] {option}\n"

    while True:
        pretty("HEADER", title_buffer)
        pretty("BOLD", buffer)
        i, option, code = optionHandler(input())
        if i == -1:
            print("Invalid Action")
        else:
            exec(code)


# Handles the display menus - easily updateable.
def optionHandler(option: str = None) -> tuple[int, str, str]:
    try:
        choice: int = int(option)  # type: ignore
    except:
        return -1, "NOP", "pass"

    if choice >= len(OPTIONS) or choice < 0:
        return -1, "NOP", "pass"

    return OPTIONS[choice]


# Option to display About.
def about() -> None:
    try:
        with open("about.txt", "r", encoding="utf-8") as f:
            lines = f.read()
        print(lines)
    except:
        pretty(
            "WARNING", "The file (about.txt) could not be found in top level directory"
        )


if __name__ == "__main__":
    main()
