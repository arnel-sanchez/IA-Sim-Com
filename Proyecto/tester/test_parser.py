from os.path import dirname, abspath
from sys import path
from unittest import TestCase, main


SCRIPT_DIR = dirname(abspath(__file__))
path.append(dirname(SCRIPT_DIR))


class TestParser(TestCase):
    def test_A(self):
        self.assertEqual(1, 1)

    def test_B(self):
        self.assertEqual(1, 1)

    def test_C(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    main()
