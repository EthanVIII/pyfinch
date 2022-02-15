class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pretty(type:str, text:str) -> None:
    b = col
    if type == "INFO":
        print(col.OKGREEN + "[INFO] " + col.ENDC + text)
    elif type == "HEADER":
        print(col.OKGREEN + text + col.ENDC)
    elif type == "WARNING":
        print(col.WARNING + "[WARNING] " + col.ENDC + text)
    elif type == "PANIC":
        print(col.FAIL + "[PANIC] " + text + col.ENDC )
        quit()
    elif type == "BOLD":
        print(col.BOLD + text + col.BOLD)
    elif type == "SPRT":
        print(col.OKBLUE + "----- " + text + " -----" +col.ENDC)
    else:
        print(col.WARNING + "[WARNING] " + col.ENDC + "No pretty format for: " + text[0:3] + "...")