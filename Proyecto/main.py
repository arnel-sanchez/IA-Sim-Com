from tokenizer import tokenize


def main():
    tokens = tokenize("if;point else point22; 22 3.4; point_1 point;\"AAA\"aaa\n123.0 _a.a")
    print()
    for token in tokens:
        token.print_token()
        print()


if __name__ == '__main__':
    main()
