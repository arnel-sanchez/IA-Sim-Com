from os.path import dirname, abspath
from sys import path
from unittest import TestCase, main


SCRIPT_DIR = dirname(abspath(__file__))
path.append(dirname(SCRIPT_DIR))
from compilation.tokenizer import Tokenizer
from compilation.tokens import TokenType, Token


class TestTokenizer(TestCase):
    def test_A(self):
        tokenizer = Tokenizer()
        file, text = "console", "a=1;"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = [Token(TokenType.T_ID, 1, 1, "a"), Token(TokenType.T_ASSIGN, 1, 2),
                      Token(TokenType.T_I_VALUE, 1, 3, 1), Token(TokenType.T_SEMICOLON, 1, 4)]
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1, t2)

    def test_B(self):
        tokenizer = Tokenizer()
        file, text = "console", "if;point else point22; 22 3.4; point_1 point;\"AAA\"aaa\n123.0 _a.a"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = [Token(TokenType.T_IF, 1, 1), Token(TokenType.T_SEMICOLON, 1, 3),
                      Token(TokenType.T_ID, 1, 4, "point"), Token(TokenType.T_ELSE, 1, 10),
                      Token(TokenType.T_ID, 1, 15, "point22"), Token(TokenType.T_SEMICOLON, 1, 22),
                      Token(TokenType.T_I_VALUE, 1, 24, "22"), Token(TokenType.T_D_VALUE, 1, 27, "3.4"),
                      Token(TokenType.T_SEMICOLON, 1, 30), Token(TokenType.T_ID, 1, 32, "point_1"),
                      Token(TokenType.T_ID, 1, 40, "point"), Token(TokenType.T_SEMICOLON, 1, 45),
                      Token(TokenType.T_S_VALUE, 1, 46, "AAA"), Token(TokenType.T_ID, 1, 51, "aaa"),
                      Token(TokenType.T_D_VALUE, 2, 1, "123.0"), Token(TokenType.T_ID, 2, 7, "_a"),
                      Token(TokenType.T_DOT, 2, 9), Token(TokenType.T_ID, 2, 10, "a")]
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1, t2)

    def test_C(self):
        tokenizer = Tokenizer()
        file, text = "console", "a=1;"
        tokens, error = tokenizer.tokenize(file, text)
        tokens_ref = [Token(TokenType.T_ID, 1, 1, "a"), Token(TokenType.T_ASSIGN, 1, 2),
                      Token(TokenType.T_I_VALUE, 1, 3, 1), Token(TokenType.T_SEMICOLON, 1, 4)]
        for i in range(len(tokens)):
            t1 = str(tokens[i])
            t2 = str(tokens_ref[i])
            self.assertEqual(t1, t2)


if __name__ == '__main__':
    main()
