import unittest
from unittest.mock import MagicMock
from code_interpreter import isCodeLine, codeInterpreter
from machine_client import MachineClient


class TestInterpreterMethods(unittest.TestCase):

    def test_skippingLines(self):
        self.assertFalse(isCodeLine("%"))
        self.assertFalse(isCodeLine("(Here I'm commenting the G-Code)"))
        self.assertFalse(isCodeLine("O12345"))
        self.assertFalse(isCodeLine(""))

    def test_greatLines(self):
        self.assertTrue("N4 T01 M06")

    def test_homeIsCalled(self):
        thing = MachineClient()
        thing.home = MagicMock()
        itemList = ["N01", "G20", "M30"]
        codeInterpreter(itemList, thing)

        self.assertTrue(thing.home.called)

    def test_xyzIsCalled(self):
        thing = MachineClient()
        thing.move = MagicMock()
        thing.move_x = MagicMock()
        thing.move_y = MagicMock()
        thing.move_z = MagicMock()
        itemList = ["N01", "X20.", "Y30.5", "Z22"]
        codeInterpreter(itemList, thing)

        self.assertTrue(thing.move.called)
        self.assertFalse(thing.move_x.called)
        self.assertFalse(thing.move_y.called)
        self.assertFalse(thing.move_z.called)
        thing.move.assert_called_once_with(20.0, 30.5, 22.0)

    def test_xzIsCalled(self):
        thing = MachineClient()
        thing.move = MagicMock()
        thing.move_x = MagicMock()
        thing.move_y = MagicMock()
        thing.move_z = MagicMock()
        itemList = ["N01", "X.2", "Z-30.", "G22"]
        codeInterpreter(itemList, thing)

        self.assertFalse(thing.move.called)
        self.assertTrue(thing.move_x.called)
        self.assertFalse(thing.move_y.called)
        self.assertTrue(thing.move_z.called)
        thing.move_x.assert_called_once_with(0.2)
        thing.move_z.assert_called_once_with(-30.0)

    def test_valueErrorInGcode(self):
        thing = MachineClient()
        thing.move_x = MagicMock()
        itemList = ["N01", "Xx"]
        codeInterpreter(itemList, thing)

        self.assertFalse(thing.move_x.called)


if __name__ == '__main__':
    unittest.main()
