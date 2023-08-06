from typing import Union, List, Mapping, Dict, Optional
from collections import defaultdict
from copy import copy

from .ast import Node, Field, NodeField, NodeListField, call, NodeRefField
from .reader import Reader
from .ast.visitor import NodeVisitor, visitor

import ast as pyast


class NoMatch(Exception):
    def __init__(self, expr, pos, reader):
        self.expr = expr
        self.pos = pos
        self.reader = reader
        super().__init__()

    def __str__(self):
        return f"{self.expr.as_grammar()} doesn't match at {self.pos}"

    def __or__(self, other):
        if other.pos > self.pos:
            return other
        return self


class ParseNode(Node):
    reader = Field()


class ParseSlice(ParseNode):
    start: int = Field(0)
    end: Optional[int] = Field(default=None)

    def __init__(self, start: int, end: Optional[int], reader):
        self._bytes = None
        super().__init__(start=start, end=end, reader=reader)

    def __bytes__(self):
        return bytes(self.reader[self.start:self.end])

    def __str__(self):
        return self.__bytes__().decode("utf-8")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    def __bool__(self):
        return self.start != self.end


class Token(ParseSlice):
    pass


class PseudoToken(Token):
    """
    PseudoToken behaves like a token, but the string and bytes representation
    is fixed, and doesn't rely on the backing Reader.
    """

    def __init__(self, start, end, content, reader):
        super().__init__(start=start, end=end, reader=reader)
        self.content = content
        self.str_content = self.content.decode("utf-8")

    def __bytes__(self):
        return self.content

    def __str__(self):
        return self.str_content


class Expr(Node):
    "A PEG expression"


class Discard(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        return self.expression(reader)

    def as_grammar(self, atomic=False):
        return "-{}".format(self.expression.as_grammar(True))


class Seq(Expr):
    expressions = NodeListField()

    def __init__(self, *exprs, **kwargs):
        super().__init__(expressions=exprs, **kwargs)

    def __call__(self, reader: Reader):
        results = []
        for expr in self.expressions:
            result = expr(reader)
            if not isinstance(expr, Discard):
                results.append(result)
        return results

    def as_grammar(self, atomic=False):
        g = " ".join([e.as_grammar(True) for e in self.expressions])
        if atomic and len(self.expressions) > 1:
            return "( {} )".format(g)
        return g


class Choice(Expr):
    expressions = NodeListField()

    def __init__(self, *exprs, **kwargs):
        super().__init__(expressions=exprs, **kwargs)

    def __call__(self, reader: Reader):
        start = reader.pos
        exc = None
        for expr in self.expressions:
            try:
                res = expr(reader)
            except NoMatch as e:
                if exc is None:
                    exc = e
                else:
                    exc |= e
                reader.pos = start
            else:
                return res
        raise exc

    def as_grammar(self, atomic=False):
        g = " / ".join([e.as_grammar(True) for e in self.expressions])
        if atomic and len(self.expressions) > 1:
            return "( {} )".format(g)
        return g


class OneOrMore(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        results = []
        results.append(self.expression(reader))
        while True:
            start = reader.pos
            try:
                results.append(self.expression(reader))
            except NoMatch:
                reader.pos = start
                return results

    def as_grammar(self, atomic=False):
        return "{}+".format(self.expression.as_grammar(True))


class Repeat(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        results = []
        while True:
            start = reader.pos
            try:
                results.append(self.expression(reader))
            except NoMatch:
                reader.pos = start
                return results

    def as_grammar(self, atomic=False):
        return "{}*".format(self.expression.as_grammar(True))


class Optional(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        start = reader.pos
        try:
            return self.expression(reader)
        except NoMatch:
            reader.pos = start
            return Token(start, start, reader)

    def as_grammar(self, atomic=False):
        return "{}?".format(self.expression.as_grammar(True))


class LookAhead(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        start = reader.pos
        try:
            self.expression(reader)
            reader.pos = start
            return Token(start, start, reader)
        except NoMatch:
            raise

    def as_grammar(self, atomic=False):
        return "&{}".format(self.expression.as_grammar(True))


class Not(Expr):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        start = reader.pos
        try:
            self.expression(reader)
        except NoMatch:
            reader.pos = start
            return Token(start, start, reader)
        else:
            raise NoMatch(self, reader.pos, reader)

    def as_grammar(self, atomic=False):
        return "!{}".format(self.expression.as_grammar(True))


class CharRange(Expr):
    singles = Field(default=call(list))
    ranges = Field(default=call(list))

    def __init__(self, singles, ranges=None, **kwargs):
        if isinstance(singles, bytes):
            singles = singles.decode("utf-8")
        ranges = ranges if ranges is not None else []
        for r in ranges:
            if isinstance(r[0], (str, bytes)):
                r[0] = ord(r[0])
            if isinstance(r[1], (str, bytes)):
                r[1] = ord(r[1])
        super().__init__(singles=singles, ranges=ranges, **kwargs)

    def __call__(self, reader: Reader):
        start = reader.pos
        n = reader.next_rune()
        if n is None:
            raise NoMatch(self, start, reader)
        n = bytes(n).decode("utf-8")
        if n in self.singles:
            return Token(start, reader.pos, reader)
        n = ord(n)
        for r in self.ranges:
            if r[0] <= n <= r[1]:
                return Token(start, reader.pos, reader)
        raise NoMatch(self, start, reader)

    def char_to_str(self, char):
        if char == "\t":
            return r"\t"
        if char == "\n":
            return r"\n"
        if char == "\r":
            return r"\r"
        # if char == "\x1d":
            # return "\]"
        o = ord(char)
        if o > 127:
            res = f"{o:x}"
            if len(res) <= 2:
                return f"\\x{o:02x}"
            if len(res) <= 4:
                return f"\\u{o:04x}"
            if len(res) <= 8:
                return f"\\U{o:04x}"
            assert False
        return char

    def as_grammar(self, atomic=False):
        gr = "["
        singles = self.singles
        if "-" in singles:
            gr = gr + "-"
            singles = singles.replace("-", "")
        for s in singles:
            gr += self.char_to_str(s)
        for r in self.ranges:
            gr += self.char_to_str(
                    chr(r[0])) + "-" + self.char_to_str(chr(r[1]))
        gr += "]"
        return gr


class AnyChar(Expr):
    def __call__(self, reader):
        start = reader.pos
        n = reader.next_rune()
        if n is not None:
            return Token(start, reader.pos, reader)
        raise NoMatch(self, reader.pos, reader)

    def as_grammar(self, atomic=False):
        return "."


class Literal(Expr):
    lit = Field(initarg=True)
    ignorecase = Field(default=False)

    def __init__(self, lit: Union[bytes, str], ignorecase: bool = False,
                 **kwargs):
        if isinstance(lit, str):
            lit = lit.encode("utf-8")
        if ignorecase:
            lit = lit.lower()
        super().__init__(lit=lit, ignorecase=ignorecase, **kwargs)

    def __call__(self, reader):
        start = reader.pos
        if self.lit == b"":
            return b""
        len_ = len(self.lit)
        prefix = reader.read(len_)
        if prefix is not None:
            if self.ignorecase:
                if prefix.lower() == self.lit:
                    return Token(start, reader.pos, reader)
            elif prefix == self.lit:
                return Token(start, reader.pos, reader)
            else:
                raise NoMatch(self, reader.pos-len_, reader)
        raise NoMatch(self, reader.pos, reader)

    def as_grammar(self, atomic=False):
        lit = self.lit.decode("utf-8")
        lit = lit.replace("\\", "\\\\")
        lit = lit.replace("\a", "\a")
        lit = lit.replace("\b", "\b")
        lit = lit.replace("\t", "\t")
        lit = lit.replace("\n", "\n")
        lit = lit.replace("\f", "\f")
        lit = lit.replace("\r", "\r")
        lit = lit.replace("\v", "\v")
        ignore = self.ignorecase and "i" or ""
        if lit != '"':
            return '"{}"{}'.format(lit, ignore)
        return """'"'%s""" % ignore


class Label(Expr):
    name = Field(initarg=True)
    expression = Field(initarg=True)

    def __call__(self, reader: Reader):
        result = self.expression(reader)
        reader._action_context[self.name] = result
        return result

    def as_grammar(self, atomic=False):
        return "{}:{}".format(self.name, self.expression.as_grammar(True))


class LabelsExtractor(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.names = []

    @visitor(Label)
    def visit_label(self, n: Label):
        self.names.append(n.name)

    def __call__(self, e: Expr):
        self.visit(e)
        return self.names


class ActionFunc:
    def __init__(self, def_: str, names: List[str] = None, namespace=None):
        if namespace is None:
            namespace = {}
        self.str_def = def_
        self.names = names
        self.namespace = namespace

    def compile(self):
        mod = pyast.parse(self.str_def)
        # return the last expression of the definition
        if isinstance(mod.body[-1], pyast.Expr):
            mod.body[-1] = pyast.Return(value=mod.body[-1].value)
        # create a method from the definition
        args = [pyast.arg(arg="self"), pyast.arg(arg="_raw")]
        defaults = []
        for n in self.names:
            args.append(pyast.arg(arg=n))
            defaults.append(pyast.Constant(value=None))
        func = pyast.FunctionDef(
            name="__call__",
            args=pyast.arguments(
                posonlyargs=[],
                kwonlyargs=[],
                args=args,
                kw_defaults=[],
                defaults=defaults
            ),
            body=mod.body,
            decorator_list=[]
        )
        mod = pyast.Module(body=[func], type_ignores=[])
        mod = pyast.fix_missing_locations(mod)
        mod = compile(mod, "<str>", "exec")
        ns = copy(self.namespace)
        exec(mod, ns)
        self.fn = ns["__call__"]

    def __call__(self, *args, **kwargs):
        return self.fn(self, *args, **kwargs)


class Action(Expr):
    expression = NodeField(initarg=True)
    action = Field(initarg=True)

    def __init__(self, expression: Expr, action: str, **kwargs):
        super().__init__(expression, action, **kwargs)
        self._action_str = str(action)
        if isinstance(action, str):
            self.action = ActionFunc(action, [])

    def compile(self, names, ns):
        if isinstance(self.action, ActionFunc):
            self.action.names = names
            self.action.namespace = ns
            self.action.compile()

    def __call__(self, reader: Reader):
        ctx = getattr(reader, "_action_context", None)
        if ctx is None:
            reader._action_context = {}
        else:
            reader._action_context = copy(ctx)
        result = self.expression(reader)
        result = self.action(result, **reader._action_context)
        reader._action_context = ctx
        return result

    def as_grammar(self, atomic=False):
        g = f"{self.expression.as_grammar(True)} {{ {self._action_str} }}"
        if atomic:
            return f"( {g} )"
        else:
            return g


class Rule(Expr):
    name = Field(initarg=True)
    rule = NodeRefField(default=None)

    def __call__(self, reader: Reader):
        ctx = reader._action_context
        reader._action_context = {}
        try:
            result = self.rule(reader)
        finally:
            reader._action_context = ctx
        return result

    def as_grammar(self, atomic=False):
        return self.name


class RuleDef(Node):
    name = Field(initarg=True)
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        return self.expression(reader)

    def as_grammar(self, atomic=False):
        return f"{self.name} <- {self.expression.as_grammar()}"

    def as_ref(self):
        return f"Rule `{self.name}`"


class RuleVisitor(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.rules: Dict[str, RuleDef] = {}
        self.required: Mapping[str, List[Rule]] = defaultdict(list)

    @visitor(Rule)
    def visit_rule(self, n: Rule):
        self.required[n.name].append(n)

    @visitor(RuleDef)
    def visit_ruledef(self, n: RuleDef):
        self.rules[n.name] = n

    def __call__(self, r: Node):
        self.visit(r)
        for name, refs in self.required.items():
            for r in refs:
                r.rule = self.rules[name]


class RuleSet(Node):
    rules = NodeListField(default=call(list))
    name = Field(default=None)
    entrypoint = Field(default=None)

    def __init__(self, *rules, name: str = None, entrypoint: str = None):
        if rules and entrypoint is None:
            entrypoint = rules[0].name
        super().__init__(rules=rules, name=name, entrypoint=entrypoint)
        RuleVisitor()(self)

    def __call__(self, reader: Reader, entrypoint: str = None):
        entrypoint = entrypoint if entrypoint is not None else self.entrypoint
        if entrypoint is None:
            raise ValueError("No entrypoint found")
        for r in self.rules:
            if r.name == entrypoint:
                return r(reader)
        raise ValueError(f"Entrypoint `{ entrypoint }` not found")

    def as_grammar(self, atomic=False):
        return "\n".join([r.as_grammar() for r in self.rules])


class OpExpr(Expr):
    gen = NodeField(default=None, optional=True)
    operators = NodeListField(default=call(list))
    actions = Field(default=call(list))

    def compile(self, ns):
        for action in self.actions:
            if isinstance(action, ActionFunc):
                action.names = ["x"]
                action.namespace = ns
                action.compile()


class InfixOpExpr(OpExpr):
    def compile(self, ns):
        for action in self.actions:
            if isinstance(action, ActionFunc):
                action.names = ["lhs", "rhs"]
                action.namespace = ns
                action.compile()


class LeftAssocInfix(InfixOpExpr):
    def __init__(self, gen, ops):
        operators = [o[0] for o in ops]
        actions = []
        for o in ops:
            if isinstance(o[1], str):
                actions.append(ActionFunc(o[1]))
            else:
                actions.append(o[1])
        super().__init__(gen=gen, operators=operators, actions=actions)

    def __call__(self, reader: Reader, left=None):
        if left is None:
            left = self.gen(reader)
        start = reader.pos
        for i, o in enumerate(self.operators):
            try:
                op = o(reader)
            except NoMatch:
                reader.pos = start
                continue
            else:
                right = self.gen(reader)
                left = self.actions[i]([left, op, right], left, right)
                return self(reader, left)
        return left

    def as_grammar(self, atomic=False):
        lines = ["\n  |--"]
        for i, o in enumerate(self.operators):
            lines.append(
                f"  | @' {o.as_grammar()} @ {{ {self.actions[i].str_def} }}")
        return "\n".join(lines)


class RightAssocInfix(InfixOpExpr):
    def __init__(self, gen, ops):
        operators = [o[0] for o in ops]
        actions = []
        for o in ops:
            if isinstance(o[1], str):
                actions.append(ActionFunc(o[1]))
            else:
                actions.append(o[1])
        super().__init__(gen=gen, operators=operators, actions=actions)

    def __call__(self, reader: Reader):
        left = self.gen(reader)
        start = reader.pos
        for i, o in enumerate(self.operators):
            try:
                op = o(reader)
            except NoMatch:
                reader.pos = start
                continue
            else:
                right = self(reader)
                return self.actions[i]([left, op, right], left, right)
        return left

    def as_grammar(self, atomic=False):
        lines = ["\n  |--"]
        for i, o in enumerate(self.operators):
            lines.append(
                f"  | @ {o.as_grammar()} @' {{ {self.actions[i].str_def} }}")
        return "\n".join(lines)


class Postfix(OpExpr):
    def __init__(self, gen, ops):
        operators = [o[0] for o in ops]
        actions = []
        for o in ops:
            if isinstance(o[1], str):
                actions.append(ActionFunc(o[1]))
            else:
                actions.append(o[1])
        super().__init__(gen=gen, operators=operators, actions=actions)

    def __call__(self, reader: Reader, left=None):
        if left is None:
            left = self.gen(reader)
        start = reader.pos
        for i, o in enumerate(self.operators):
            try:
                op = o(reader)
            except NoMatch:
                reader.pos = start
                continue
            else:
                left = self.actions[i]([left, op], x=left)
                return self(reader, left)
        return left

    def as_grammar(self, atomic=False):
        lines = ["\n  |--"]
        for i, o in enumerate(self.operators):
            lines.append(
                f"  | @ {o.as_grammar()} {{ {self.actions[i].str_def} }}")
        return "\n".join(lines)


class Prefix(OpExpr):
    def __init__(self, gen, ops):
        operators = [o[0] for o in ops]
        actions = []
        for o in ops:
            if isinstance(o[1], str):
                actions.append(ActionFunc(o[1]))
            else:
                actions.append(o[1])
        super().__init__(gen=gen, operators=operators, actions=actions)

    def __call__(self, reader: Reader):
        start = reader.pos
        for i, o in enumerate(self.operators):
            try:
                op = o(reader)
            except NoMatch:
                reader.pos = start
                continue
            else:
                right = self(reader)
                return self.actions[i]([op, right], x=right)
        return self.gen(reader)

    def as_grammar(self, atomic=False):
        lines = ["\n  |--"]
        for i, o in enumerate(self.operators):
            lines.append(
                f"  | {o.as_grammar()} @ {{ {self.actions[i].str_def} }}")
        return "\n".join(lines)


class PrecedenceRule(RuleDef):
    name = Field(initarg=True)
    rules = NodeListField(initarg=True)
    expression = Field(default=None)

    def __init__(self, name, *rules):
        _rules = list(rules)
        atoms = []

        while _rules:
            if isinstance(_rules[-1], OpExpr):
                break
            atoms.insert(0, _rules.pop(-1))
        if not atoms:
            raise ValueError("missing atoms in precedence climbing")
        if len(atoms) == 1:
            _rules.extend(atoms)
        else:
            atom = Choice(*atoms)
            _rules.append(atom)

        rules = []
        gen = None
        idx = len(_rules)
        for r in reversed(_rules):
            new = RuleDef(f"{name}_{idx}", r)
            if gen is not None:
                r.gen = Rule(gen.name, rule=gen)
            gen = new
            rules.append(new)
            idx -= 1
        rules.reverse()
        super().__init__(name, rules, None)

    def compile(self, ns):
        for r in self.rules[:-1]:
            r.expression.compile(ns)

    def __call__(self, reader: Reader):
        return self.rules[0](reader)

    def as_grammar(self, atomic=False):
        result = f"{self.name} <- "
        result += "".join([r.expression.as_grammar() for r in self.rules[:-1]])
        result += "\n  |--\n  | "
        result += "\n  | ".join([e.as_grammar() for e in self.rules[-1].expression.expressions])
        return result


def flatten(lst):
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result


class Slice(Node):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        result = self.expression(reader)
        result = flatten(result)
        return Token(result[0].start, result[-1].end, reader)

    def as_grammar(self, atomic=False):
        return "${}".format(self.expression.as_grammar(True))


class Concat(Node):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        result = self.expression(reader)
        result = flatten(result)
        return PseudoToken(
                result[0].start, result[-1].end,
                b"".join([bytes(t) for t in result]), reader)

    def as_grammar(self, atomic=False):
        return "$${}".format(self.expression.as_grammar(True))


class Breakpoint(Node):
    expression = NodeField(initarg=True)

    def __call__(self, reader: Reader):
        import ipdb
        ipdb.set_trace()
        return self.expression(reader)

    def as_grammar(self, atomic=False):
        return "%{}".format(self.expression.as_grammar(True))


# ## Nice to have
# class Debug - implemented as an action ?
# class Regex
# class Position
# class Expect (^"name")
# class Quiet
# add delim (**, ++) and ranges (X<n,m>, X<n> with X in [*, **, +, ++])
