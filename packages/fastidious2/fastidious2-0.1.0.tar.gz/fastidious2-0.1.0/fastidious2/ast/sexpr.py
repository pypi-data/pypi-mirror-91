from typing import Any
from .visitor import NodeVisitor, visitor
from .field import Node, NodeList, NodeRefField
from io import StringIO


class SexprGen(NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent = 0
        self.buf = None

    def __call__(self, n):
        self.buf = StringIO()
        self.visit(n)
        return self.buf.getvalue()

    def nl(self):
        self.buf.write("\n")
        self.buf.write("  " * self.indent)

    @visitor(Node)
    def visit_node(self, n: Node):
        self.buf.write("( ")
        self.buf.write(n.__class__.__name__)
        self.indent += 1
        for (name, field) in n.__class__.__meta__.fields.items():
            self.nl()
            self.buf.write(name)
            self.buf.write(": ")
            if isinstance(field, NodeRefField):
                val = getattr(n, name)
                if val is not None:
                    self.buf.write(getattr(n, name).as_ref())
                else:
                    self.buf.write("None")
            else:
                self.visit(getattr(n, name))
        self.indent -= 1
        self.buf.write(" )")
        return False

    @visitor(NodeList)
    def visit_nodelist(self, n: NodeList):
        self.buf.write("[ ")
        self.indent += 1
        for item in n:
            self.nl()
            self.visit(item)
        self.indent -= 1
        self.buf.write(" ]")
        return False

    def visit_generic(self, g: Any):
        self.buf.write(str(g))


def sexpr(n: Node):
    return SexprGen()(n)
