# print colors.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorize_info(str):
    return bcolors.BOLD+bcolors.OKBLUE + str + bcolors.ENDC

def colorize_success(str):
    return bcolors.BOLD+bcolors.OKGREEN + str + bcolors.ENDC

def colorize_fail(str):
    return bcolors.BOLD+bcolors.FAIL + str + bcolors.ENDC

def colorize_warning(str):
    return bcolors.BOLD+bcolors.WARNING + str + bcolors.ENDC
