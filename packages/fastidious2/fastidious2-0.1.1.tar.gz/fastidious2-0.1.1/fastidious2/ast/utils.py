from collections.abc import Iterable
from .field import Node, Field, NodeList


def children(n: Node) -> Iterable[Field]:
    def gen(n: Node):
        for _, v in n.__data__.items():
            if isinstance(v, Node):
                yield v
            elif isinstance(v, NodeList):
                for vv in v:
                    yield vv
    return iter(gen(n))
