# gcode-interpreter
A Python program that reads a G-Code program file and parses the instructions. Based on the instructions read, Machine Client API is called.

Run file cnc.py and give G-Code file as an argument
```
$ python cnc.py rectangle.gcode
```

Tested on Python 3.9.7 on Linux

The project includes unit tests
```
$ python unittests.py
```

Author: Tiina Karhukivi