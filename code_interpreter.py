"""
G-Code interpreter methods.
Author: Tiina Karhukivi
"""


def codeInterpreter(itemList, client):
    """ Interpret G-Code Lines
        Args:
        itemList (list[str]): List of G-Codes from a row
        client (MachineClient): Client for API calls
    """

    # Check special case: Are X, Y and Z all present in a row?
    xFound = False
    yFound = False
    zFound = False
    for item in itemList:
        if item.find("X") != -1:
            xFound = True
        elif item.find("Y") != -1:
            yFound = True
        elif item.find("Z") != -1:
            zFound = True

    xyzFound = (xFound and yFound and zFound)

    for item in itemList:
        if (len(item) < 2):
            continue

        initial = item[0]
        value = item[1:]

        if not value.isdigit():
            try:
                float(value)
            except:
                print("Error: Value is not digit in", item, "at", itemList)
                return

        if initial == "X":
            if xyzFound:
                xVal = value
            else:
                client.move_x(float(value))
        elif initial == "Y":
            if xyzFound:
                yVal = value
            else:
                client.move_y(float(value))
        elif initial == "Z":
            if xyzFound:
                client.move(float(xVal), float(yVal), float(value))
            else:
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


def isCodeLine(line):
    """ Check if line includes G-Code commands
        Args:
        line (str): Row from a file
    """

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
