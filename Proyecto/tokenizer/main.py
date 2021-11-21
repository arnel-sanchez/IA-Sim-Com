from tokenizer import Tokenizer


def main():
    tokenizer = Tokenizer()

    file, text = "console", "if;point else point22; 22 3.4; point_1 point;\"AAA\"aaa\n123.0 _a.a"
    print("\n" + text)

    tokens, error = tokenizer.tokenize(file, text)
    print()
    if error is not None:
        print(error)
    else:
        for token in tokens:
            print(token)


if __name__ == '__main__':
    main()
