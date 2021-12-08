import unittest
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from compilation.tokenizer import Tokenizer
from compilation.tokens import TokenType, Token

class Test_tokenizer(unittest.TestCase):
    def test_A(self):
        tokenizer = Tokenizer()
        file, text = "console","a"
        tokens, error = tokenizer.tokenize(file, text)
        t1 = str(tokens[0])
        t2 = str(Token(TokenType.T_ID, 1,1, "a"))
        self.assertEqual(t1,t2)

if __name__ == '__main__':
    unittest.main()
