import unittest

import llutils.Greetings as Greetings

class Test(unittest.TestCase):
    def test_reverse_name(self):
        greet = Greetings("Lukas")
        self.assertEqual(greet.name, "Lukas")
        greet.reverse_name()
        self.assertEqual(greet.name, "Sakul")

if __name__ == "__main__":
    Test().test_reverse_name()