from compilation.ast.nodes import Node
from compilation.ast.operations import AddOp, SubOp, MulOp, DivOp, ModOp, ExpOp
from compilation.context import Context


class NodeE(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) > 0:
            self.ast = self.hijos[1].ast

    def checktype(self, context: Context):
        return self.ast.checktype(context)

    def validate(self, context: Context):
        return self.ast.validate(context)


class NodeB(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 2:
            self.ast = self.hijos[1].ast


class NodeX(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            if isinstance(self.hijos[0], NodeAdd):
                if isinstance(self.padre, NodeX):
                    self.ast: Node = AddOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = AddOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeSub):
                if isinstance(self.padre, NodeX):
                    self.ast: Node = SubOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = SubOp(self.padre.hijos[0].ast, self.hijos[2].ast)

        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeX):
                self.ast: Node = self.padre.hijos[1].ast
            else:
                self.ast: Node = self.padre.hijos[0].ast


class NodeM(Node):
    def __init__(self, *args, **kwargs):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            self.ast = self.hijos[1].ast
        elif len(self.hijos) == 1:
            self.ast = self.hijos[0].ast
        else:
            self.ast = None


class NodeY:
    def __init__(self):
        self.ast = None
        self.padre = None
        self.hijos = list()

    def refreshAST(self):
        if len(self.hijos) == 3:
            if isinstance(self.hijos[0], NodeMult):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = MulOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = MulOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeDiv):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = DivOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = DivOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeMod):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ModOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ModOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeExp):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ExpOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ExpOp(self.padre.hijos[0].ast, self.hijos[2].ast)
        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeY):
                self.ast = self.padre.hijos[1].ast
            else:
                self.ast = self.padre.hijos[0].ast


class NodeQ(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 1:
            self.ast = self.hijos[0]


class NodeEpsilon(Node):
    def __init__(self):
        self.padre = None

    @staticmethod
    def type() -> str:
        return "EXP"


class NodeMult(Node):
    @staticmethod
    def type() -> str:
        return "MUL"


class NodeDiv(Node):
    @staticmethod
    def type() -> str:
        return "DIV"


class NodeMod(Node):
    @staticmethod
    def type() -> str:
        return "MOD"


class NodeExp(Node):
    @staticmethod
    def type() -> str:
        return "EXP"


class NodeAdd(Node):
    @staticmethod
    def type() -> str:
        return "ADD"


class NodeSub(Node):
    @staticmethod
    def type() -> str:
        return "SUB"
