import sys
from machine_client import MachineClient


def isCodeLine(line):

    cleanLine = line.strip()

    # Empty Row
    if len(cleanLine) == 0:
        return False

    # Begin/End Mark
    if cleanLine[0] == "%":
        return False

    # Program Number
    if cleanLine[0] == "O":
        return False

    # Comment Line
    if cleanLine[0] == "(":
        return False

    return True


def codeInterpreter(code, client):

    initial = code[0]
    value = code[1:]

    if initial == "X":
        client.move_x(float(value))
    elif initial == "Y":
        client.move_y(float(value))
    elif initial == "Z":
        client.move_z(float(value))
    elif initial == "F":
        client.set_feed_rate(float(value))
    elif initial == "S":
        client.set_spindle_speed(int(value))
    elif initial == "M":
        if value == "8" or value == "08":
            client.coolant_on()
        elif value == "9" or value == "09":
            client.coolant_off()
        elif value == "30":
            client.home()
    elif initial == "T":
        client.change_tool(value)


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

        for item in itemList:

            if (len(item) < 2):
                continue

            codeInterpreter(item, mc)


if __name__ == '__main__':
    main(sys.argv[1:])
