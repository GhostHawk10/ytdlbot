import unittest
from commands.atom import *

class TestAtom(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, broadcast, 3)
        self.assertRaises(TypeError, broadcast, False)
        self.assertRaises(TypeError, broadcast, 1+2j)
        self.assertRaises(TypeError, broadcast, 2.1)
        self.assertRaises(TypeError, broadcast, None)
