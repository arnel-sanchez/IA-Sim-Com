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
        file, text = "console","a=1;"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = []
        tokens_ref.append(Token(TokenType.T_ID, 1,1, "a"))
        tokens_ref.append(Token(TokenType.T_ASSIGN, 1,2))
        tokens_ref.append(Token(TokenType.T_I_VALUE, 1,3, 1))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,4))
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1,t2)
    
    def test_B(self):
        tokenizer = Tokenizer()
        file, text = "console", "if;point else point22; 22 3.4; point_1 point;\"AAA\"aaa\n123.0 _a.a"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = []
        tokens_ref.append(Token(TokenType.T_IF, 1,1))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,3))
        tokens_ref.append(Token(TokenType.T_ID, 1,4, "point"))
        tokens_ref.append(Token(TokenType.T_ELSE, 1,10))
        tokens_ref.append(Token(TokenType.T_ID, 1,15, "point22"))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,22))
        tokens_ref.append(Token(TokenType.T_I_VALUE, 1,24, "22"))
        tokens_ref.append(Token(TokenType.T_D_VALUE, 1,27, "3.4"))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,30))
        tokens_ref.append(Token(TokenType.T_ID, 1,32, "point_1"))
        tokens_ref.append(Token(TokenType.T_ID, 1,40, "point"))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,45))
        tokens_ref.append(Token(TokenType.T_S_VALUE, 1,46, "AAA"))
        tokens_ref.append(Token(TokenType.T_ID, 1,51, "aaa"))
        tokens_ref.append(Token(TokenType.T_D_VALUE, 2,1, "123.0"))
        tokens_ref.append(Token(TokenType.T_ID, 2,7, "_a"))
        tokens_ref.append(Token(TokenType.T_DOT, 2,9))
        tokens_ref.append(Token(TokenType.T_ID, 2,10, "a"))
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1,t2)

    def test_C(self):
        tokenizer = Tokenizer()
        file, text = "console","a=1;"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = []
        tokens_ref.append(Token(TokenType.T_ID, 1,1, "a"))
        tokens_ref.append(Token(TokenType.T_ASSIGN, 1,2))
        tokens_ref.append(Token(TokenType.T_I_VALUE, 1,3, 1))
        tokens_ref.append(Token(TokenType.T_SEMICOLON, 1,4))
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1,t2)

if __name__ == '__main__':
    unittest.main()
