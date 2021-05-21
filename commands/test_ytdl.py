import unittest
from commands.ytdl import *

class TestYtdl(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, ytdl_get, 3)
        self.assertRaises(TypeError, ytdl_get, False)
        self.assertRaises(TypeError, ytdl_get, 1+2j)
        self.assertRaises(TypeError, ytdl_get, 2.1)
        self.assertRaises(TypeError, ytdl_get, None)
