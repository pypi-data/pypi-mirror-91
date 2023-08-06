from types import SimpleNamespace
from typing import Union, Any, List
from collections.abc import Iterable

UNSET = object


class call:
    def __init__(self, fn):
        self.fn = fn


class Field:
    def __init__(self, default: Any = UNSET, initarg : bool = False):
        self.name = None
        self.pos = None
        self.default = default
        self.initarg = initarg

    def __get__(self, inst: Any, owner=None):
        if inst is None:
            return self
        try:
            return inst.__data__[self.name]
        except KeyError:
            default = self.default
            if default is UNSET:
                raise AttributeError(self.name)
            if isinstance(default, call):
                return default.fn()
            return default

    def __set__(self, inst, value):
        inst.__data__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
        self.pos = len(owner.__meta__.fields)
        owner.__meta__.fields[name] = self


class ListField(Field):
    "Marker class Fields that accept lists"
    pass


class NodeMeta(type):
    def __new__(cls, name, bases, args):
        # print(cls, name, bases, args)
        fields = {}
        for b in bases:
            if isinstance(b, cls):
                fields |= b.__meta__.fields
        initargs = []
        for b in reversed(bases):
            if isinstance(b, cls):
                initargs.extend(b.__meta__.initargs)
        metadata = SimpleNamespace(fields=fields)
        args["__meta__"] = metadata
        newcls = type.__new__(cls, name, bases, args)
        newargs = []
        for k, v in args.items():
            if isinstance(v, Field) and v.initarg:
                try:
                    initargs.remove(k)
                except ValueError:
                    pass
                newargs.append(k)
        newcls.__meta__.initargs = newargs + initargs
        return newcls


class Node(metaclass=NodeMeta):
    __meta__ = SimpleNamespace(fields={}, initarg=[])

    def __init__(self, *args, **kwargs):
        if args:
            ia = self.__class__.__meta__.initargs
            if len(ia) < len(args):
                raise TypeError(f"__init__() takes { len(ia) } positional "
                                f"arguments but { len(args) } were given")
            for i, name in enumerate(ia):
                # print(self)
                # print(name)
                # import ipdb; ipdb.set_trace()
                if name in kwargs:
                    raise TypeError("__init__() got mutliple values for "
                                    f"argument '{ name }'")
                kwargs[name] = args[i]
        self.__data__ = dict()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, o):
        if self.__class__ is o.__class__:
            for f in self.__class__.__meta__.fields:
                if getattr(self, f) != getattr(o, f):
                    return False
            return True
        return False


class NodeList(list):
    def __init__(self, arg=None):
        if arg is None:
            return super().__init__()
        super().__init__(arg)
        if not isinstance(arg, NodeList):
            if not all(isinstance(i, Node) for i in self):
                raise TypeError("Parameter must be an iterable of Nodes")

    def extend(self, other: "NodeList"):  # type: ignore[override]
        if not isinstance(other, NodeList):
            other = NodeList(other)
        return super().extend(other)

    def append(self, item: Node):
        if not isinstance(item, Node):
            raise TypeError(
                    f"Parameter must be a Node, not { item.__class__ }")


class NodeField(Field):
    def __init__(self, *args, optional=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.optional = optional

    def __set__(self, inst: Node, value: Node):
        if not isinstance(value, Node) and not self.optional:
            raise TypeError(
                    f"`{ inst.__class__.__name__ }.{self.name } must "
                    "be a Node instance")
        inst.__data__[self.name] = value


class NodeRefField(NodeField):
    pass


class NodeListField(ListField):
    def __set__(self, inst: Node, value: Union[List[Node], NodeList]):
        if not isinstance(value, NodeList):
            value = NodeList(value)
        return super().__set__(inst, value)


if __name__ == "__main__":
    class Truc(Node):
        bidule = Field(initarg=True)
        hop = Field(default=42)
        ff = Field(default=call(list))

    assert isinstance(Truc, NodeMeta)

    class Sub(Truc):
        tata = Field(initarg=True)

    assert isinstance(Truc, NodeMeta)

    t = Truc(bidule="toto")
    assert t.bidule == "toto"
    assert t.hop == 42
    assert t.ff == []

    s = Sub("tt", "bb", hop=43)
    assert s.tata == "tt"
    assert s.bidule == "bb"
    assert s.hop == 43
    assert s.ff == []



