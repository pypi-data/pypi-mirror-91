import unittest

import llutils.Greetings as Greetings

class Test(unittest.TestCase):
    def test_reverse_name(self):
        self.assertEqual(Greetings("Lukas").reverse_name.name == "Sakul")