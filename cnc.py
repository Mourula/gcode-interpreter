import sys


def isCodeLine(line):

    cleanLine = line.strip()

    # Empty Row
    if len(cleanLine) == 0:
        return False

    # Program Number
    if cleanLine[0] == "O":
        return False

    # Comment Line
    if cleanLine[0] == "(":
        return False

    return True


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

    if filerows.count("%") != 2:
        print("ERROR: Begin/End marking error")
        return

    for row in filerows:
        cleanline = row.strip()
        if(cleanline == "%"):
            continue

        # -- Debug --
        # items = cleanline.split()
        # for item in items:
        #    print(item)

    print("-- Done --")


if __name__ == '__main__':
    main(sys.argv[1:])
