from compilation.tokens import Token


class Node:
    def __init__(self):
        pass


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__()
        self.token = token

    def __repr__(self):
        return self.token.string()


class BinOptNode(Node):
    def __init__(self, left_token: Token, opt_token: Token, right_token: Token):
        super().__init__()
        self.left_token = left_token
        self.opt_token = opt_token
        self.right_token = right_token

    def __repr__(self):
        return "({}, {}, {})".format(self.left_token.string(), self.opt_token.string(), self.right_token.string())


class AssignNode(Node):
    def __init__(self, id_token: Token, assign_token: Token, expression: Token):
        super().__init__()
        #self.left_token = left_token
        #self.opt_token = opt_token
        #self.right_token = right_token

    def __repr__(self):
        return "({}, {}, {})".format(self.left_token.string(), self.opt_token.string(), self.right_token.string())
