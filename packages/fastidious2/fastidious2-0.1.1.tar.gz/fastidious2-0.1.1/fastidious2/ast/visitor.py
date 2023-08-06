from typing import Callable, Dict, List, Any
from .field import Node, NodeList, NodeRefField


class visitor:
    def __init__(self, *nodecls):
        self.nodecls = nodecls

    def __call__(self, fn):
        fn.is_visitor_of = self.nodecls
        return fn


class Visitor:
    _visitors: Dict[type, Callable] = {}

    def __init_subclass__(cls):
        old_visitors = cls._visitors
        visitors = {}
        for name in dir(cls):
            if callable((meth := getattr(cls, name))):
                node_types = getattr(meth, "is_visitor_of", None)
                if node_types:
                    for node_type in node_types:
                        visitors[node_type] = meth

        cls._visitors = old_visitors | visitors

    def _get_visitor(self, n):
        # cache method lookup
        searched: List[type] = []
        for c in n.__class__.mro():
            if c in self.__class__._visitors:
                meth = self.__class__._visitors[c]
                for c in searched:
                    self.__class__._visitors[c] = meth
                break
            searched.append(c)
        else:
            meth = self.__class__.visit_generic
        return meth

    def visit_generic(self, n: Node):
        pass


class NodeVisitor(Visitor):
    def __init__(self, once=True):
        self.once = once
        self.visited = set()
        self.current_field_name = None
        self.list_field = False
        self.is_ref = False

    @visitor(NodeList)
    def visit_nodelist_field(self, n: NodeList):
        field_name = self.current_field_name
        list_field = self.list_field
        for sub in n:
            self.list_field = True
            self.visit(sub)
            self.current_field_name = field_name
        self.list_field = list_field

    def visit(self, n: Any):
        if self.once and isinstance(n, Node):
            if not self.is_ref:
                if id(n) in self.visited:
                    return
                self.visited.add(id(n))

        meth = self._get_visitor(n)

        result = meth(self, n)
        if self.is_ref:
            self.is_ref = False
        if result is not False and isinstance(n, Node):
            self.visit_subnodes(n)

    def visit_subnodes(self, n: Node):
        for field_name, field in n.__class__.__meta__.fields.items():
            try:
                val = getattr(n, field_name)
            except AttributeError:
                continue
            self.current_field_name = field_name
            if isinstance(field, NodeRefField):
                self.is_ref = True
            self.visit(val)

    def visit_generic(self, n: Node):
        return True


class FieldVisitor(NodeVisitor):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.fieldname = None


