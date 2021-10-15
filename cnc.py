import sys
from machine_client import MachineClient
from code_interpreter import codeInterpreter, isCodeLine

"""
Main for the G-Code interpreter.
Author: Tiina Karhukivi
"""


def main(args):

    if len(args) < 1:
        print("ERROR: Give G-Code file as an argument.")
        return

    filename = args[0]

    try:
        with open(filename) as gcodefile:
            # Read only lines that have G-Code
            filerows = list(
                filter(isCodeLine, gcodefile.read().splitlines()))
    except Exception as exep:
        print("ERROR: Cannot read the file")
        print(exep)
        return

    if len(filerows) == 0:
        print("ERROR: Empty file.")
        return

    mc = MachineClient()

    for row in filerows:
        cleanRow = row.strip()
        itemList = cleanRow.split()

        codeInterpreter(itemList, mc)


if __name__ == '__main__':
    main(sys.argv[1:])
